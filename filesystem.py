from encrypt import Encrypt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
'''
allows the user to create new files, read files and edit/save files
'''
class FileSystem:
    def __init__(self):
        pass

    def isNewOrganisation(self, organisation):
        # check if organisation.key exists localkeys directory
        keyPath = 'localkeys/'+organisation+'.key'
        isNew = False
        try:
            keyFile = open(keyPath)
        except IOError:
            isNew = True
        finally:
            return isNew

    def createOrganisation(self, organisation):
        keyPath = 'localkeys/'+organisation+'.key'
        enc = Encrypt()
        # enc.privateKey needs to be saved
        pem = enc.privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
        )
        with open(keyPath, 'wb') as f:
            f.write(pem)

    def getOrganisationKey(self, organisation):
        keyPath = 'localkeys/'+organisation+'.key'
        privateKey = None
        with open(keyPath, 'rb') as key_file:
            privateKey = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
            )

    def import_file(self, filepath, savepath, organisation):
        # first check if the organisation is is a new one
        isNew = self.isNewOrganisation(organisation)
        if isNew:
            self.createOrganisation(organisation)

        # read the file they provided, encrypt the contents and save it
        original_file = open(filepath, 'r')
        original_contents = original_file.read()
        original_file.close()

        # load the key for the organisation
        key = self.getOrganisationKey(organisation)
        enc = Encrypt(key)
        encrypted_contents = enc.encrypt_string(original_contents)
        encrypted_file = open(savepath, 'wb')
        encrypted_file.write(encrypted_contents)
        encrypted_file.close()


if __name__ == '__main__':
    f = FileSystem()
    f.import_file('test.py', 'test.py.enc', 'Student Hack')
