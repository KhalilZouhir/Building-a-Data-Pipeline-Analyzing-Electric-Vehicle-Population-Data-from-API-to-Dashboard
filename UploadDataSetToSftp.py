import paramiko
import requests
import csv

# Replace 'your_api_url_here' with the actual URL of the API
api_url = 'https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD'

api_key = "XXXXXXXXXXX"

params = {
    'api_key': api_key,
}

# Make a request to the API to get the CSV data
response = requests.get(api_url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the CSV data from the response content
    csv_data = response.text

    # Specify the file path where you want to save the CSV file
    file_path = '/home/kali/Electric_Vehicle_Population_Data.csv'

    # Open the file in write mode
    with open(file_path, 'a', newline='') as csvfile:
        # Create a CSV writer
        csv_writer = csv.writer(csvfile)

        # Split the CSV data into lines and write them to the CSV file
        for line in csv_data.split('\n'):
            csv_writer.writerow(line.split(','))

    print(f"DataSet retrieved successfully from the API to local machine at /home/kali/Electric_Vehicle_Population_Data.csv")
else:
    print(f"Failed to retrieve data from API. Status code: {response.status_code}")
    print(response.text)  # Print the error message if any

# Create SSH client
ssh_client = paramiko.SSHClient()

# Remote server credentials
host = "192.168.1.4"
username = "sftp_user"
password = "kali"
port = 2222

# Set missing host key policy to automatically add unknown hosts
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Establish SSH connection to the remote server
ssh_client.connect(hostname=host, port=port, username=username, password=password)

# Open an SFTP session within the established SSH connection
ftp = ssh_client.open_sftp()

# Upload the local file to the remote server using SFTP
files = ftp.put("/home/kali/Electric_Vehicle_Population_Data.csv", "/uploads/Electric_Vehicle_Population_Data.csv")

# Close the SFTP session and SSH connection
ftp.close()
ssh_client.close()
print("Dataset uploaded successfully to sftp-server")
