from encrypt import Encrypt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
'''
allows the user to create new files, read files and edit/save files
'''
class FileSystem:
    def __init__(self, localkeyspath='localkeys'):
        self.local_keys_path = localkeyspath

    def isNewOrganisation(self, organisation):
        # check if organisation.key exists localkeys directory
        keyPath = self.local_keys_path+'/'+organisation+'.key'
        isNew = False
        try:
            keyFile = open(keyPath)
        except IOError:
            isNew = True
        finally:
            return isNew

    def createOrganisation(self, organisation, password):
        keyPath = self.local_keys_path+'/'+organisation+'.key'
        enc = Encrypt()
        password = bytes(password, encoding='utf-8')
        # enc.privateKey needs to be saved
        pem = enc.privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password)
        )
        with open(keyPath, 'wb') as f:
            f.write(pem)

    def getOrganisationKey(self, organisation, password):
        keyPath = self.local_keys_path+'/'+organisation+'.key'
        privateKey = None
        password = bytes(password, encoding='utf-8')
        with open(keyPath, 'rb') as key_file:
            privateKey = serialization.load_pem_private_key(
            key_file.read(),
            password=password,
            backend=default_backend()
            )
        return privateKey

    def importFile(self, filepath, organisation, password, savepath=None):
        # first check if the organisation is is a new one
        if self.isNewOrganisation(organisation):
            self.createOrganisation(organisation, password)

        # read the file they provided, encrypt the contents and save it
        original_file = open(filepath, 'r')
        original_contents = original_file.read()
        original_file.close()

        # load the key for the organisation
        key = self.getOrganisationKey(organisation, password)
        enc = Encrypt(key)
        encrypted_contents = enc.encrypt_string(original_contents)
        savepath = savepath+'.enc' if savepath == None else savepath
        encrypted_file = open(savepath, 'wb')
        encrypted_file.write(encrypted_contents)
        encrypted_file.close()

    def readFile(self, filepath, organisation, password):
        # get the key for the provided organisation
        key = self.getOrganisationKey(organisation, password)
        enc = Encrypt(key)

        encrypted_file = open(filepath, 'rb')
        encrypted_contents = encrypted_file.read()
        encrypted_file.close()

        decrypted_contents = enc.decrypt_string(encrypted_contents)
        return decrypted_contents

    def updateFile(self, filepath, contents, organisation, password):
        # self function can be used when the user chooses to save their work
        # get the key for the provided organisation
        key = self.getOrganisationKey(organisation, password)
        enc = Encrypt(key)

        encrypted_file = open(filepath, 'wb')
        encrypted_contents = enc.encrypt_string(contents)
        encrypted_file.write(encrypted_contents)
        encrypted_file.close()

    def createFile(self, filepath, organisation, password):
        # make an empty file
        self.updateFile(filepath, '', organisation, password)


if __name__ == '__main__':
    f = FileSystem()
    f.importFile('test.py', 'Student Hack', 'test1234', 'test.py.enc')
    print(f.readFile('test.py.enc', 'Student Hack', 'test1234'))
    f.updateFile('test.py.enc', 'print("hello world 1")', 'Student Hack',
    'test1234')
    print(f.readFile('test.py.enc', 'Student Hack', 'test1234'))
    f.createFile('test1.py.enc', 'Student Hack', 'test1234')
