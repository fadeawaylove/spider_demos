import subprocess

infile = 'test/1.ts'
outfile = '1.mp4'

subprocess.run(['ffmpeg', '-i', infile, outfile])