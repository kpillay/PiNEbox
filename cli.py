# cli.py simply runs the main function within PiNe_master - more efficient when packaging a bundle
# Kirubin Pillay 01/12/2020

from PiNe_master import main
from verSet import verSet

if __name__ == '__main__':
    inst = verSet()
    inst.__init__()
    main(inst.ver, inst.releaseDate, inst.dev)
