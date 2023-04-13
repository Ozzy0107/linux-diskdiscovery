import subprocess
import glob
import textwrap
import argparse


class ScanDisks:

    def __init__(self, args, par=False):
        self.args = args
        self.par = par

        if self.par is False or self.args.scan:
            self.path = "/sys/class/scsi_host/*/scan"
        else:
            self.path = "/sys/class/scsi_device/*/device/rescan"

    def execscan(self):

        files = glob.glob(self.path)

        for file in files:
            try:
                subprocess.run(['echo', '\"- - -\"', '>', file], shell=True)
                print("Finished!")
            except Exception as e:
                print(f'Error {e}')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="New disk scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            '''
            Simply run the program on the command line to scan recently added disks
            or use -r or --rescan to rescan existing disks
            '''
        )
    )

    parser.add_argument('-r', '--rescan', help='Scan existing disks', nargs='?', const=True)
    parser.add_argument('-s', '--scan', help='Scan for new disks. This is the default behaviour', nargs='?', const=True)

    args = parser.parse_args()
    parexists = True

    if not (args.rescan and args.scan):
        parexists = False

    sd = ScanDisks(args, parexists)
    sd.execscan()
