import sys
from capstone import *
import binascii

from elftools.elf.constants import SH_FLAGS
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection

##############################################################
# takes a string of arbitrary length and formats it 0x for Capstone
def convertXCS(s):
    if len(s) < 2: 
        print "Input too short!"
        return 0
    
    if len(s) % 2 != 0:
        print "Input must be multiple of 2!"
        return 0

    conX = ''
    
    for i in range(0, len(s), 2):
        b = s[i:i+2]
        b = chr(int(b, 16))
        conX = conX + b
    return conX


##############################################################


def getHexStreamsFromElfExecutableSections(filename):
    print "Processing file:", filename
    with open(filename, 'rb') as f:
        elffile = ELFFile(f)
        
        execSections = []
        goodSections = [".text"] #[".interp", ".note.ABI-tag", ".note.gnu.build-id", ".gnu.hash", ".hash", ".dynsym", ".dynstr", ".gnu.version", ".gnu.version_r", ".rela.dyn", ".rela.plt", ".init", ".plt", ".text", ".fini", ".rodata", ".eh_frame_hdr", ".eh_frame"]
        checkedSections = [".init", ".plt", ".text", ".fini"]
        
        for nsec, section in enumerate(elffile.iter_sections()):

            # check if it is an executable section containing instructions
            
            # good sections we know so far:
            #.interp .note.ABI-tag .note.gnu.build-id .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rela.dyn .rela.plt .init .plt .text .fini .rodata .eh_frame_hdr .eh_frame
        
            if section.name not in goodSections:
                continue
            
            # add new executable section with the following information
            # - name
            # - address where the section is loaded in memory
            # - hexa string of the instructions
            name = section.name
            addr = section['sh_addr']
            byteStream = section.data()
            hexStream = binascii.hexlify(byteStream)
            newExecSection = {}
            newExecSection['name'] = name
            newExecSection['addr'] = addr
            newExecSection['hexStream'] = hexStream
            execSections.append(newExecSection)

        return execSections


if __name__ == '__main__':
    if sys.argv[1] == '-length' and sys.argv[3] == '--test':
    	length = int(sys.argv[2])
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        for filename in sys.argv[4:]:
            r = getHexStreamsFromElfExecutableSections(filename)
            print "Found ", len(r), " executable sections:"
            i = 0
            for s in r:
            	i += 1
                
                hexdata = s['hexStream']
                gadget = hexdata           
                gadget = convertXCS(gadget)
                offset = 0
                list_gadgets = []
                temp = []
                for (address, size, mnemonic, op_str) in md.disasm_lite(gadget, offset):
                    if mnemonic[:3] == 'ret':
                    	temp.append((str(hex(address)[:-1]),str(size),str(mnemonic), str(op_str)))
                    	if len(temp)>length:
                    		t = temp[(len(temp)-length-1):]
                    		list_gadgets.append(t)
                    		#if one wants to print the gadgets as string
                    		"""
                    		gad = ''
                    		i = 0
                    		for x in t:
                    			if i == 0:
                    				gad = x[0] + ': ' + x[2] + ' ' + x[3]
                    			else:
                    				gad = gad + ', ' + x[2] + ' ' + x[3]
                    			i+=1
                    		list_gadgets.append(gad)
                    		"""
                    	temp = []
                    elif mnemonic[0] == 'j':
                    	temp = []
                    else:
                    	temp.append((str(hex(address)[:-1]),str(size),str(mnemonic), str(op_str)))
                print('\n'.join(map(str, list_gadgets)))
                print len(list_gadgets)

def compare(myGadgets, ROP_file):
	count = 0
	for x in myGadgets:
		if ROP_file.count(x[0][2:]) > 0:
			count +=1
	return count