"""
Blockchain Integration
NFT dövme sertifikaları için blockchain entegrasyonu
"""

import json
import hashlib
from datetime import datetime
from web3 import Web3
from eth_account import Account
import requests

class TattooNFTCertificate:
    """Dövme NFT sertifikası sınıfı"""
    
    def __init__(self, web3_provider, contract_address, private_key):
        self.w3 = Web3(Web3.HTTPProvider(web3_provider))
        self.contract_address = contract_address
        self.account = Account.from_key(private_key)
        self.contract = self.w3.eth.contract(
            address=contract_address,
            abi=self.get_contract_abi()
        )
    
    def get_contract_abi(self):
        """NFT kontrat ABI'si"""
        return [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "safeTransferFrom",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "string", "name": "tokenURI", "type": "string"}
                ],
                "name": "mintCertificate",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [
                    {"internalType": "uint256", "name": "tokenId", "type": "uint256"}
                ],
                "name": "tokenURI",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def create_certificate_metadata(self, appointment, design, customer):
        """NFT metadata oluştur"""
        metadata = {
            "name": f"{design.title} - Dövme Sertifikası",
            "description": f"{design.description}\n\nSanatçı: {design.artist.name}\nMüşteri: {customer.name}\nTarih: {appointment.date_time.strftime('%d.%m.%Y')}",
            "image": design.image_url,
            "attributes": [
                {
                    "trait_type": "Artist",
                    "value": design.artist.name
                },
                {
                    "trait_type": "Style",
                    "value": design.style
                },
                {
                    "trait_type": "Category",
                    "value": design.category
                },
                {
                    "trait_type": "Date",
                    "value": appointment.date_time.strftime('%Y-%m-%d')
                },
                {
                    "trait_type": "Duration",
                    "value": f"{appointment.duration} minutes"
                },
                {
                    "trait_type": "Price",
                    "value": f"₺{appointment.total_price}"
                },
                {
                    "trait_type": "Studio",
                    "value": "Tattoo Studio"
                },
                {
                    "trait_type": "Certificate Type",
                    "value": "Authenticity"
                }
            ],
            "external_url": f"https://tattoostudio.com/certificate/{appointment.id}",
            "background_color": "1a1a1a"
        }
        
        return metadata
    
    def upload_to_ipfs(self, metadata):
        """Metadata'ı IPFS'e yükle"""
        try:
            # IPFS API çağrısı (basit örnek)
            ipfs_api = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
            
            headers = {
                "Content-Type": "application/json",
                "pinata_api_key": "YOUR_PINATA_API_KEY",
                "pinata_secret_api_key": "YOUR_PINATA_SECRET_KEY"
            }
            
            response = requests.post(
                ipfs_api,
                json=metadata,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                return f"https://gateway.pinata.cloud/ipfs/{result['IpfsHash']}"
            else:
                print(f"IPFS yükleme hatası: {response.text}")
                return None
                
        except Exception as e:
            print(f"IPFS yükleme hatası: {e}")
            return None
    
    def mint_certificate(self, appointment, design, customer):
        """NFT sertifikası mint'le"""
        try:
            # Metadata oluştur
            metadata = self.create_certificate_metadata(appointment, design, customer)
            
            # IPFS'e yükle
            token_uri = self.upload_to_ipfs(metadata)
            
            if not token_uri:
                return None
            
            # NFT mint'le
            transaction = self.contract.functions.mintCertificate(token_uri).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Transaction'ı imzala
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            
            # Transaction'ı gönder
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Transaction'ı bekle
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Token ID'yi al
            logs = self.contract.events.CertificateCreated().process_receipt(tx_receipt)
            token_id = logs[0]['args']['tokenId']
            
            return {
                'token_id': token_id,
                'tx_hash': tx_hash.hex(),
                'token_uri': token_uri,
                'owner': customer.email,
                'created_at': datetime.utcnow()
            }
            
        except Exception as e:
            print(f"NFT mint'leme hatası: {e}")
            return None
    
    def verify_certificate(self, token_id):
        """Sertifikayı doğrula"""
        try:
            # Token URI'yi al
            token_uri = self.contract.functions.tokenURI(token_id).call()
            
            # Metadata'yı IPFS'ten al
            response = requests.get(token_uri)
            
            if response.status_code == 200:
                metadata = response.json()
                return {
                    'valid': True,
                    'metadata': metadata,
                    'token_uri': token_uri
                }
            else:
                return {'valid': False, 'error': 'Metadata bulunamadı'}
                
        except Exception as e:
            return {'valid': False, 'error': str(e)}
    
    def transfer_certificate(self, token_id, to_address):
        """Sertifikayı transfer et"""
        try:
            transaction = self.contract.functions.safeTransferFrom(
                self.account.address,
                to_address,
                token_id
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'from': self.account.address,
                'to': to_address,
                'token_id': token_id
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

class DigitalTattooRegistry:
    """Dijital dövme kayıt sistemi"""
    
    def __init__(self):
        self.certificates = {}
        self.blockchain_enabled = False
        
    def enable_blockchain(self, web3_provider, contract_address, private_key):
        """Blockchain entegrasyonunu aktif et"""
        self.nft_certificate = TattooNFTCertificate(web3_provider, contract_address, private_key)
        self.blockchain_enabled = True
    
    def register_tattoo(self, appointment, design, customer):
        """Dövmeyi kaydet"""
        certificate_data = {
            'appointment_id': appointment.id,
            'design_id': design.id,
            'customer_id': customer.id,
            'artist_id': design.artist.id,
            'created_at': datetime.utcnow(),
            'verified': False
        }
        
        # Blockchain aktifse NFT mint'le
        if self.blockchain_enabled:
            nft_result = self.nft_certificate.mint_certificate(appointment, design, customer)
            
            if nft_result:
                certificate_data.update({
                    'nft_token_id': nft_result['token_id'],
                    'nft_tx_hash': nft_result['tx_hash'],
                    'nft_token_uri': nft_result['token_uri'],
                    'blockchain_verified': True
                })
        
        # Sertifikayı veritabanına kaydet
        certificate_id = self.save_certificate(certificate_data)
        
        return {
            'certificate_id': certificate_id,
            'nft_data': nft_result if self.blockchain_enabled else None,
            'verified': True
        }
    
    def verify_tattoo(self, certificate_id):
        """Dövme sertifikasını doğrula"""
        certificate = self.get_certificate(certificate_id)
        
        if not certificate:
            return {'valid': False, 'error': 'Sertifika bulunamadı'}
        
        # Blockchain doğrulaması
        if certificate.get('nft_token_id') and self.blockchain_enabled:
            nft_verification = self.nft_certificate.verify_certificate(certificate['nft_token_id'])
            
            if nft_verification['valid']:
                return {
                    'valid': True,
                    'certificate': certificate,
                    'blockchain_data': nft_verification['metadata']
                }
            else:
                return {'valid': False, 'error': 'Blockchain doğrulaması başarısız'}
        
        # Standart doğrulama
        return {
            'valid': True,
            'certificate': certificate
        }
    
    def get_certificate_qr_data(self, certificate_id):
        """QR kod için veri oluştur"""
        certificate = self.get_certificate(certificate_id)
        
        if not certificate:
            return None
        
        qr_data = {
            'certificate_id': certificate_id,
            'verification_url': f"https://tattoostudio.com/verify/{certificate_id}",
            'appointment_id': certificate['appointment_id'],
            'design_id': certificate['design_id'],
            'customer_id': certificate['customer_id'],
            'created_at': certificate['created_at']
        }
        
        if certificate.get('nft_token_id'):
            qr_data.update({
                'nft_token_id': certificate['nft_token_id'],
                'blockchain_url': f"https://etherscan.io/tx/{certificate['nft_tx_hash']}"
            })
        
        return json.dumps(qr_data)
    
    def save_certificate(self, certificate_data):
        """Sertifikayı kaydet (veritabanı işlemi)"""
        # Gerçek uygulamada veritabanı kaydı yapılır
        certificate_id = f"cert_{datetime.utcnow().timestamp()}"
        self.certificates[certificate_id] = certificate_data
        return certificate_id
    
    def get_certificate(self, certificate_id):
        """Sertifikayı getir"""
        return self.certificates.get(certificate_id)

# Kullanım örneği
if __name__ == "__main__":
    # Dijital kayıt sistemini başlat
    registry = DigitalTattooRegistry()
    
    # Blockchain entegrasyonu (opsiyonel)
    # registry.enable_blockchain(
    #     "https://mainnet.infura.io/v3/YOUR_PROJECT_ID",
    #     "0x...NFT_CONTRACT_ADDRESS",
    #     "YOUR_PRIVATE_KEY"
    # )
    
    # Dövme kaydetme örneği
    # certificate_result = registry.register_tattoo(appointment, design, customer)
    
    # Doğrulama örneği
    # verification_result = registry.verify_tattoo(certificate_result['certificate_id'])
