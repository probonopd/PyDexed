# http://yates.ca/dx7/

class pced:

    """
    A PCED (Performance Edit) object contains the data for a single performance edit.
    Documented on page Add-10 of the DX7II manual.
    PCED = PMEM format is 51 bytes long?
    """
    def __init__(self):
        self.plmd = 1 # 0/1/2: Single/Dual/Split
        self.vnma = 0 # A channel voice number; 0 .. 127
        self.vnmb = 0 # B channel voice number; 0 .. 127
        self.mctb = 0
        self.mcky = 0
        self.mcsw = 0
        self.ddtn = 0 # Dual detune; 0 .. 7
        self.sppt = 60 # Split point; 0 .. 127
        self.fdmp = 0 # 0/1: Off/On
        self.sfsw = 3 # Sustain Foot Switch Bit 0: A, Bit 1: B, 0/1: Off/On
        self.fsas = 1 # Foot Switch Assign 0: SUS, 1: POR, 2: KHLD, 3: SFT
        self.fsw = 3 # Foot Switch Bit 0: A, Bit 1: B, 0/1: Off/On
        self.sprng = 0 # 0 .. 7
        self.nsfta = 24 # 0 .. 48
        self.nsftb = 24 # 0 .. 48
        self.blnc = 0 # 0 .. 100 # Volume Balance (-50 .. +50)
        self.tvlm = 0 # 0 .. 99 # Total Volume
        self.csld1 = 0 # 0 .. 105 # Control Slider 1
        self.csld2 = 0 # 0 .. 105 # Control Slider 2
        self.cssw = 0 # 0 .. 3 # Continuous Slider Assign Switch
        self.pnmd = 1 # 0 .. 3 # Pan Mode 0: Mix, 1: On On, 2: On Off, 3: Off On
        self.panrng = 0 # 0 .. 99 # Pan Controll Range
        self.panasn = 1 # 0 .. 2 # Pan Controll Assign 0/1/2: LFO/Velocity/Key#
        self.pnegr1 = 99 # 0 .. 99 # Pan EG Rate 1
        self.pnegr2 = 99
        self.pnegr3 = 99
        self.pnegr4 = 99
        self.pnegl1 = 50
        self.pnegl2 = 50
        self.pnegl3 = 50
        self.pnegl4 = 50
        self.pnam = "INIT PERF           " # 20 characters

    def get_bytes(self):
        # 51 bytes
        bytes = []
        for field in [self.plmd, self.vnma, self.vnmb, self.mctb, self.mcky, self.mcsw, self.ddtn, self.sppt, \
                      self.fdmp, self.sfsw, self.fsas, self.fsw, self.sprng, self.nsfta, self.nsftb, self.blnc, \
                        self.tvlm, self.csld1, self.csld2, self.cssw, self.pnmd, self.panrng, self.panasn, self.pnegr1, \
                            self.pnegr2, self.pnegr3, self.pnegr4, self.pnegl1, self.pnegl2, self.pnegl3, self.pnegl4]:
            bytes.append(field)
        padded_name_padded = self.pnam.ljust(20, ' ')
        for c in padded_name_padded:
            bytes.append(ord(c))

        assert len(bytes) == 51

        return bytes
    
    def set_bytes(self, bytes):
        assert len(bytes) == 51

        self.plmd = bytes[0]
        self.vnma = bytes[1]
        self.vnmb = bytes[2]
        self.mctb = bytes[3]
        self.mcky = bytes[4]
        self.mcsw = bytes[5]
        self.ddtn = bytes[6]
        self.sppt = bytes[7]
        self.fdmp = bytes[8]
        self.sfsw = bytes[9]
        self.fsas = bytes[10]
        self.fsw = bytes[11]
        self.sprng = bytes[12]
        self.nsfta = bytes[13]
        self.nsftb = bytes[14]
        self.blnc = bytes[15]
        self.tvlm = bytes[16]
        self.csld1 = bytes[17]
        self.csld2 = bytes[18]
        self.cssw = bytes[19]
        self.pnmd = bytes[20]
        self.panrng = bytes[21]
        self.panasn = bytes[22]
        self.pnegr1 = bytes[23]
        self.pnegr2 = bytes[24]
        self.pnegr3 = bytes[25]
        self.pnegr4 = bytes[26]
        self.pnegl1 = bytes[27]
        self.pnegl2 = bytes[28]
        self.pnegl3 = bytes[29]
        self.pnegl4 = bytes[30]
        self.pnam = bytes[31:].decode('ascii')

class PerformanceSyx:

    def __init__(self, filename):
        self.pceds = []
        for i in range(32):
            self.pceds.append(pced())
        with open(filename, "rb") as f:
            bytes = f.read() # 1650 bytes = 51 bytes * 32 PCEDs + 18 bytes
        assert len(bytes) == 1650
        # Skip the first 16 bytes
        bytes = bytes[16:]
        # Discard the last 2 bytes
        bytes = bytes[:-2]
        # Populate self.pceds with the 32 PCEDs
        for i in range(32):
            self.pceds[i].set_bytes(bytes[i*51:(i+1)*51])

def main():
    PCED = pced()
    print(PCED.get_bytes())

    # Read a PCED from a file
    PS = PerformanceSyx("DX7IIFDPerf.SYX")
    for i in range(32):
        print(PS.pceds[i].pnam)


if __name__ == "__main__":
    main()