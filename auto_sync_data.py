import subprocess, os

def main():
    if 'BELL128' in str(subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], stdout=subprocess.PIPE).stdout):
        os.system('scp root@dietpi:~/temp_history.csv /Users/matt/Projects/TempTracker/')
    else:
        pass

if __name__ == '__main__':
    main()
