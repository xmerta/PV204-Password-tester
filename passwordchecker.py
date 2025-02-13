# https://haveibeenpwned.com/API/v2

import pwnedpasswords

import requests
import hashlib


def check_password(password_to_test):
    digest = hashlib.sha1(password_to_test.encode("utf8")).hexdigest()
    digest = digest.upper()  # shall be '21BD12DC183F740EE76F27B78EB39C8AD972A757' for 'P@ssw0rd'
    prefix = digest[0:5]  # shall be '21BD1' for 'P@ssw0rd'
    suffix = digest[5:]  # shall be '2DC183F740EE76F27B78EB39C8AD972A757' for 'P@ssw0rd'

    response = requests.get("https://api.pwnedpasswords.com/range/" + prefix)
    # print all passwords within the range (same hash prefix)
    # print(response.text)

    for record in response.text.upper().split("\r\n"):
        hashed, count = record.split(":")

        if suffix == hashed:
            # print(password_to_test + " detected " + str(count) + "x")
            return count
            break


def main():
    # simple version using pwnedpasswords wrapper
    # pwnedpasswords.check("P@ssw0rd")

    # step by step 'manual' version
    file_path = "passwords.txt"
    with open(file_path, 'r') as file:
        dict = {}
        for line in file:
            pswd = line.split()[0]
            dict[pswd] = check_password(pswd)

        srtddict = sorted(dict.items(), key=lambda item: int(item[1]), reverse=True)
        for i in srtddict:
            print(i)


if __name__ == "__main__":
    main()
