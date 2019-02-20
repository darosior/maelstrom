import apt, subprocess

deps = ['libzbar-dev', 'cmake', 'python3-pip', 'build-essential', 'git', 'python3', 'python3-dev', 'ffmpeg', 'libsdl2-dev', 'libsdl2-image-dev', 'libsdl2-mixer-dev', 'libsdl2-ttf-dev', 'libportmidi-dev', 'libswscale-dev', 'libavformat-dev', 'libavcodec-dev', 'zlib1g-dev', 'libgstreamer1.0-0', 'gstreamer1.0-plugins-base', 'gstreamer1.0-plugins-good', 'xclip', 'xsel']
to_install = []

packages_list = apt.Cache()
for dep in deps:
    try:
        packages_list.get(dep).is_installed
    except:
        to_install.append(dep)
        pass

if to_install:
    packages = ' '.join(to_install)
    print('T\033[1;33mThe following dependencies have to be installed : \033[0m' + packages)
    print('\033[0;34mRunning su -c \'apt install ' + packages + '\'\033[0m')
    subprocess.Popen(['su -c \'apt install '+packages+'\''], shell=True).communicate()
