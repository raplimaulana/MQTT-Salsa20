import math

class Salsa20:

    def __init__(self,key,nonce,plain_length):        
        if len(key) != 64:
            raise ValueError('Invalid key length, must be 64 byte!')
        self.key = key  
        
        if len(nonce) != 16:
            raise ValueError("Invalid nonce, must be 16 byte!")
        self.nonce = nonce
        
        self.round = 20
        self.const = "657870616e642033322d62797465206b"
        self.block = "1ff0203f0f535da1"
        self.counterBlock = "{0:016x}".format(math.ceil(plain_length / 64))
        self.initialState()
        self.salsaCore()

    def initialState(self):
        self.x = []
        self.state = []

        self.x.append(self.littleEndian(int(self.const[0:8], 16)))
        # x[1]
        self.x.append(self.littleEndian(int(self.key[0:8], 16)))
        # x[2]
        self.x.append(self.littleEndian(int(self.key[8:16], 16)))
        # x[3]
        self.x.append(self.littleEndian(int(self.key[16:24], 16)))
        # x[4]
        self.x.append(self.littleEndian(int(self.key[24:32], 16)))
        # x[5]
        self.x.append(self.littleEndian(int(self.const[8:16], 16)))
        # x[6]
        self.x.append(self.littleEndian(int(self.nonce[0:8], 16)))
        # x[7]
        self.x.append(self.littleEndian(int(self.nonce[8:16], 16)))
        # x[8]
        self.x.append(self.littleEndian(int(self.block[0:8], 16)))
        # x[9]
        self.x.append(self.littleEndian(int(self.block[8:16], 16)))
        # x[10]
        self.x.append(self.littleEndian(int(self.const[16:24], 16)))
        # x[11]
        self.x.append(self.littleEndian(int(self.key[32:40], 16)))
        # x[12]
        self.x.append(self.littleEndian(int(self.key[40:48], 16)))
        # x[13]
        self.x.append(self.littleEndian(int(self.key[48:56], 16)))
        # x[14]
        self.x.append(self.littleEndian(int(self.key[56:64], 16)))
        # x[15]
        self.x.append(self.littleEndian(int(self.const[24:32], 16)))

        if self.x[8] == 00000000 and self.x[9] == 00000000:
            self.x[8] = self.littleEndian(int(self.counterBlock[0:8], 16))
            self.x[9] = self.littleEndian(int(self.counterBlock[8:16], 16))

        for i in range(16):
            self.state.append(self.x[i])

    def littleEndian(self,a):
        b = list(range(4))

        b[0] = a >> 24 & 0xff
        b[1] = (a >> 16) & 0xff
        b[2] = (a >> 8) & 0xff
        b[3] = a & 0xff

        return b[0] + 2 ** 8 * b[1] + 2 ** 16 * b[2] + 2 ** 24 * b[3]
        
    def salsaCore(self):
        for i in range(0, self.round, 2):
            #columnround
            self.quarterRound(0,4,8,12)  # column 1
            self.quarterRound(5,9,13,1)  # column 2
            self.quarterRound(10,14,2,6)  # column 3
            self.quarterRound(15,3,7,11)  # column 4

            # rowround
            self.quarterRound(0,1,2,3)  # row 1
            self.quarterRound(5,6,7,4)  # row 2
            self.quarterRound(10,11,8,9)  # row 3
            self.quarterRound(15,12,13,14)  # row 4

        self.keystream = []

        for i in range(16):
            for j in range(8):
                self.keystream.append(self.littleEndian(self.x[i] + self.state[i]) >> (28 - 4 * j) & 0xf)
   
    def quarterRound(self,x0,x1,x2,x3):
        self.x[x1] ^= self.rotate((self.x[x0] + self.x[x3]), 7)
        self.x[x2] ^= self.rotate((self.x[x1] + self.x[x0]), 9)
        self.x[x3] ^= self.rotate((self.x[x2] + self.x[x1]), 13)
        self.x[x0] ^= self.rotate((self.x[x3] + self.x[x2]), 18)

    def rotate(self, w, z):
        return (((w << z) | ((w >> (32 - z)) & ~(0xffffffff << z))) & 0xffffffff)

    def salsaEncrypt(self, plaintext):
       plaintext = plaintext.encode("utf-8").hex()
       self.output = ""
       totalByte = len(plaintext)

       for i in range(totalByte):
           self.output += format(self.keystream[i] ^ int(plaintext[i: i + 1], 16), "x")

    def salsaDecrypt(self,ciphertext):
        self.output = ""
        totalByte = len(ciphertext)

        for i in range(totalByte):
            self.output += format(self.keystream[i] ^ int(ciphertext[i: i + 1], 16), "x")

        self.output = bytes.fromhex(self.output).decode('utf-8')

        






