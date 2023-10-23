
from netmiko import Netmiko
import pandas as pd
import csv
import re


def adding_devices():
    print("The code below needs a file name with the devices you want to add.")
    file_name = input("File Name (supported: xlsx, csv): ")
    xlsxExtension = 'xlsx'
    cscExtension = 'csv'
    pattern01 = r'[\w\.-_]+\.' + xlsxExtension + '$'
    pattern02 = r'[\w\.-_]+\.' + cscExtension + '$'
    if re.match(pattern01, file_name):
    # query01 = input("\nFile extension: ")
        devicesList = list()
        # if query01.lower() == "xlsx":
        try:
            df01 = pd.read_excel(file_name)
            df01.drop(columns=['Unnamed: 0'], inplace=True)        
            devicesList = df01.to_dict(orient='records')
        except Exception as e:
            print(e)

    elif re.match(pattern02, file_name):
        try:
            df02 = pd.read_csv(file_name)
            df02.drop(columns=['Unnamed: 0'], inplace=True)
            devicesList = df02.to_dict(orient='records')
        except Exception as a:
            print(e)
            
    else:
        return "[!] Not sure what kind of file extension you have. (supported: xlsx, csv)"
    
    return devicesList


device_List = adding_devices()

    
def make_connection(listDevices):
    ip_list, version_list, model_list, vendor_list, hostname_list = ([] for i in range(5))
    command = 'show version'

    for ip in listDevices:
        try:
            print(f"\n----Trying to login to: {ip['host']}---\n")

            net_connect = Netmiko(**ip)
            net_connect.enable()

            output = net_connect.send_command(command)
            
            version_match = re.search(r"\b\d+\.\d+\(\d+(\:\d+)?\)([A-Z]+\d+\b)?", output)
            version = version_match.group() if version_match else None
            
            model_match = re.search("Cisco (.*)\(revision", output)
            model = model_match.group(1) if model_match else None
            
            vendor_match = re.search("Cisco", output)
            vendor = vendor_match.group() if vendor_match else None

            hostname_match = re.search("(.*) uptime is", output)
            hostname = hostname_match.group(1) if hostname_match else None

            ip_list.append(ip['host'])
            version_list.append(version)
            model_list.append(model)
            vendor_list.append(vendor)
            hostname_list.append(hostname)

        except Exception:
            print(f"\n***Cannot login to: {ip['host']}***\n")
        else:
            df = pd.DataFrame({"IP Address": ip_list, "Host_Name": hostname_list, "Version": version_list, "Model": model_list, "Vendor": vendor_list})
            df.to_excel('versionList.xlsx', sheet_name='Vendors', index=False)

make_connection(device_List)



