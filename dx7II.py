# http://yates.ca/dx7/


class aced:
    """
    A ACED (Additional Parameters) object contains
    the additional DX7II parameters (in addition to the DX7 PCED voice data).
    Documented on page Add-9 of the DX7II manual.
    ACED is 74 bytes long but only 49 bytes are used, so we are only using 49 bytes.
    """
    def __init__(self):
        self.scm6 = 0 # 0 .. 1 # OP6 scaling mode normal/fraction
        self.scm5 = 0
        self.scm4 = 0
        self.scm3 = 0
        self.scm2 = 0
        self.scm1 = 0
        self.ams6 = 0 # 0 .. 7 # OP6 amplitude modulation sensitivity
        self.ams5 = 0
        self.ams4 = 0
        self.ams3 = 0
        self.ams2 = 0
        self.ams1 = 0
        self.pegr = 0 # 0 .. 3 # Pitch EG range 8va/4va/1va/1/2va
        self.ltgr = 0 # 0 .. 1 # LFO key trigger (delay) single/multi
        self.vpsw = 0 # 0 .. 1 # Pitch EG by velocity switch on/off
        self.pmod = 0 # 0 .. 3 # bit0: poly/mono, bit1: unison on/off
        self.pbr = 2 # 0 .. 12 # Pitch bend range
        self.pbs = 0 # 0 .. 12 # Breath bend step
        self.pbm = 0 # 0 .. 2 # Breath bend mode low/high/k. on
        self.rndp = 0 # 0 .. 7 # Random pitch fluctuation off/5c-41c
        self.porm = 0 # 0 .. 1 # Portamento mode ftn/fllw fngrd/flltm
        self.pqnt = 0 # 0 .. 12 # Portamento step
        self.pos = 0 # 0 .. 99 # Portamento time
        self.mwpm = 0 # 0 .. 99 # Modulation wheel pitch mod range
        self.mwam = 0 # 0 .. 99 # Modulation wheel amplitude mod range
        self.mweb = 0 # 0 .. 99 # Modulation wheel EG bias range
        self.fc1pm = 0 # 0 .. 99 # Foot controller 1 pitch mod range
        self.fc1am = 0 # 0 .. 99 # Foot controller 1 amplitude mod range
        self.fc1eb = 0 # 0 .. 99 # Foot controller 1 EG bias range
        self.fc1vl = 0 # 0 .. 99 # Foot controller 1 volume range
        self.bcpm = 0 # 0 .. 99 # Breath controller pitch mod range
        self.bcam = 0 # 0 .. 99 # Breath controller amplitude mod range
        self.bceb = 0 # 0 .. 99 # Breath controller EG bias range
        self.bcpb = 0 # 0 .. 100 # Breath controller pitch bias range
        self.atpm = 0 # 0 .. 99 # Aftertouch pitch mod range
        self.atam = 0 # 0 .. 99 # Aftertouch amplitude mod range (documentation says "ATPM"; probably a typo)
        self.ateb = 0 # 0 .. 99 # Aftertouch EG bias range
        self.atpb = 0 # 0 .. 100 # Aftertouch pitch bias range
        self.pgrs = 0 # 0 .. 7 # Pitch EG rate scaling depth
        # Bits 39-63 are reserved (null bytes)
        # self.reserved = "\x00" * 25 # 25 null bytes
        self.fc2pm = 0 # 0 .. 99 # Pitch mod range
        self.fc2am = 0 # 0 .. 99 # Amplitude mod range
        self.fc2eb = 0 # 0 .. 99 # EG bias range
        self.fc2vl = 0 # 0 .. 99 # Volume range
        self.mcpm = 0 # 0 .. 99 # Pitch mod range
        self.mcam = 0 # 0 .. 99 # Amplitude mod range
        self.mceb = 0 # 0 .. 99 # EG bias range
        self.mcvl = 0 # 0 .. 99 # Volume range
        self.udtn = 0 # 0 .. 7 # Unison detune depth
        self.fccs1 = 0 # 0 .. 99 # Foot controller 1 use as CS1 switch off/on: 0/1

    def get_bytes(self):
        # 49 bytes
        bytes = []
        for field in [self.scm6, self.scm5, self.scm4, self.scm3, self.scm2, self.scm1, self.ams6, self.ams5, self.ams4, self.ams3, \
                      self.ams2, self.ams1, self.pegr, self.ltgr, self.vpsw, self.pmod, self.pbr, self.pbs, self.pbm, self.rndp, \
                          self.porm, self.pqnt, self.pos, self.mwpm, self.mwam, self.mweb, self.fc1pm, self.fc1am, self.fc1eb, \
                              self.fc1vl, self.bcpm, self.bcam, self.bceb, self.bcpb, self.atpm, self.atam, self.ateb, self.atpb, \
                                  self.pgrs, self.fc2pm, self.fc2am, self.fc2eb, self.fc2vl, self.mcpm, self.mcam, \
                                      self.mceb, self.mcvl, self.udtn, self.fccs1]:
            bytes.append(field)
        assert len(bytes) == 49

        return bytes

    def set_bytes(self, bytes):
        assert len(bytes) == 49

        self.scm6 = bytes[0]
        self.scm5 = bytes[1]
        self.scm4 = bytes[2]
        self.scm3 = bytes[3]
        self.scm2 = bytes[4]
        self.scm1 = bytes[5]
        self.ams6 = bytes[6]
        self.ams5 = bytes[7]
        self.ams4 = bytes[8]
        self.ams3 = bytes[9]
        self.ams2 = bytes[10]
        self.ams1 = bytes[11]
        self.pegr = bytes[12]
        self.ltgr = bytes[13]
        self.vpsw = bytes[14]
        self.pmod = bytes[15]
        self.pbr = bytes[16]
        self.pbs = bytes[17]
        self.pbm = bytes[18]
        self.rndp = bytes[19]
        self.porm = bytes[20]
        self.pqnt = bytes[21]
        self.pos = bytes[22]
        self.mwpm = bytes[23]
        self.mwam = bytes[24]
        self.mweb = bytes[25]
        self.fc1pm = bytes[26]
        self.fc1am = bytes[27]
        self.fc1eb = bytes[28]
        self.fc1vl = bytes[29]
        self.bcpm = bytes[30]
        self.bcam = bytes[31]
        self.bceb = bytes[32]
        self.bcpb = bytes[33]
        self.atpm = bytes[34]
        self.atam = bytes[35]
        self.ateb = bytes[36]
        self.atpb = bytes[37]
        self.pgrs = bytes[38]
        # self.reserved = bytes[39:64]
        self.fc2pm = bytes[39]
        self.fc2am = bytes[40]
        self.fc2eb = bytes[41]
        self.fc2vl = bytes[42]
        self.mcpm = bytes[43]
        self.mcam = bytes[44]
        self.mceb = bytes[45]
        self.mcvl = bytes[46]
        self.udtn = bytes[47]
        self.fccs1 = bytes[48]


class pced:

    """
    A PCED (Performance Edit) object contains the data for a single performance edit.
    Documented on page Add-10 of the DX7II manual.
    PCED is 51 bytes long.
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
        self.nsfta = 24 # 0 .. 48 # Note Shift A
        self.nsftb = 24 # 0 .. 48 # Note Shift B
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

def aced2amem(aced):
    # Borrowed from https://github.com/rarepixel/dxconvert/blob/master/DXconvert/dx7.py
    amem = [0]*35
    amem[0] = aced[0] + (aced[1]<<1) + (aced[2]<<2) + (aced[3]<<3) + (aced[4]<<4) + (aced[5]<<5)
    amem[1] = (aced[7]<<3) + aced[6]
    amem[2] = (aced[9]<<3) + aced[8]
    amem[3] = (aced[11]<<3) + aced[10]
    amem[4] = aced[12] + (aced[13]<<2) + (aced[14]<<3) + (aced[19]<<4)
    amem[5] = (aced[16]<<2) + aced[15]
    amem[6] = (aced[18]<<4) + aced[17]
    amem[7] = (aced[21]<<1) + aced[20]
    for p in range(8, 25):
        amem[p] = aced[p+14]
    for p in range(26, 34):
        amem[p] = aced[p+13]
    amem[34] = (aced[48]<<3) + aced[47]
    for i in range(len(amem)):
        amem[i] = amem[i]&127
    assert len(amem) == 35
    return amem

def amem2aced(amem):
    # Borrowed from https://github.com/rarepixel/dxconvert/blob/master/DXconvert/dx7.py
    aced = [0]*49
    aced[0] = amem[0]&1
    aced[1] = (amem[0]&2)>>1
    aced[2] = (amem[0]&4)>>2
    aced[3] = (amem[0]&8)>>3
    aced[4] = (amem[0]&16)>>4
    aced[5] = (amem[0]&32)>>5
    aced[6] = amem[1]&0b111
    aced[7] = (amem[1]&0b111000)>>3
    aced[8] = amem[2]&0b111
    aced[9] = (amem[2]&0b111000)>>3
    aced[10] = amem[3]&0b111
    aced[11] = (amem[3]&0b111000)>>3
    aced[12] = amem[4]&0b11
    aced[13] = (amem[4]&0b100)>>2
    aced[14] = (amem[4]&0b1000)>>3
    aced[19] = (amem[4]&0b1110000)>>4
    aced[15] = amem[5]&0b11 
    aced[16] = (amem[5]&0b111100)>>2
    aced[17] = amem[6]&0b1111
    aced[18] = (amem[6]&0b110000)>>4
    aced[20] = amem[7]&1
    aced[21] = (amem[7]&0b11110)>>1
    for p in range(8, 24):
        aced[p+14] = amem[p]
    aced[38] = amem[24]&0b111
    for p in range(26, 34):
        aced[p+13] = amem[p]
    aced[47] = amem[34]&0b111
    aced[48] = (amem[34]&0b1000)>>3
    for i in range(len(aced)):
        aced[i] = aced[i]&127
    assert len(aced) == 49 # NOTE: According to the DX7II manual, ACED is 74 bytes long. This routine skips the 25 reserved bytes from the DX7II manual
    return aced

def main():
    PCED = pced()
    print(PCED.get_bytes())

    # Read a PCED from a file
    PS = PerformanceSyx("DX7IIFDPerf.SYX")
    for i in range(32):
        print(PS.pceds[i].pnam)


if __name__ == "__main__":
    main()