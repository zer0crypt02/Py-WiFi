import subprocess
import re

def get_wifi_passwords():
    """
    Windows'ta kayıtlı olan tüm WiFi şifrelerini ve ağ adlarını listeler
    """
    try:
        # Kayıtlı WiFi profillerini al
        wifi_list_command = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors='ignore')
        
        # Profil isimlerini bul
        profile_names = re.findall(r"All User Profile\s+:\s+(.*)", wifi_list_command)
        
        wifi_list = []
        
        if len(profile_names) != 0:
            for name in profile_names:
                wifi_profile = {}
                # Her profil için detaylı bilgi al
                try:
                    wifi_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name, 'key=clear']).decode('utf-8', errors='ignore')
                    # Şifre bilgisini bul
                    password = re.search(r"Key Content\s+:\s+(.*)", wifi_info)
                    
                    if password is None:
                        wifi_profile['şifre'] = 'Şifre Bulunamadı'
                    else:
                        wifi_profile['şifre'] = password.group(1)
                        
                    wifi_profile['ağ_adı'] = name
                    wifi_list.append(wifi_profile)
                except subprocess.CalledProcessError:
                    wifi_profile['ağ_adı'] = name
                    wifi_profile['şifre'] = 'Şifreye erişim engellendi'
                    wifi_list.append(wifi_profile)
                    
        return wifi_list
    
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
        return []

def main():
    print("\n=== Windows'ta Kayıtlı WiFi Ağları ===\n")
    
    wifi_data = get_wifi_passwords()
    
    if len(wifi_data) != 0:
        for i, data in enumerate(wifi_data, 1):
            print(f"{i}. Ağ Adı: {data['ağ_adı']}")
            print(f"   Şifre: {data['şifre']}")
            print('-' * 50)
    else:
        print("Kayıtlı WiFi ağı bulunamadı!")
    
    print("\nNot: Bu programı yönetici (admin) olarak çalıştırmanız önerilir.")
    input("\nÇıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()
