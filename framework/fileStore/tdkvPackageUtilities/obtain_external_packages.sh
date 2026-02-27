##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

BUILD_DIR=$1
if [  ! -d "$BUILD_DIR" ]; then
    echo "Directory does not exist"
    exit
fi

ROOT_DIR="$(pwd)"
cd $ROOT_DIR

dropbear_server="$(find . -maxdepth 2 -type d -name lib32-dropbear)"
if [ -z "${dropbear_service}" ];then
    echo "\nERROR : Provided directory is not of proper format\nexample argument : ~/rpi/build-raspberrypi4-64-rdke/tmp/work/\n"
    exit
fi

mkdir -p Packages

#Acquire gstreamer package
cd $BUILD_DIR
echo "\nAcquiring gstreamer-1.0 package"
gstreamer_dir="$(find . -maxdepth 2 -type d -name *gstreamer1.0 | grep -v nativesdk)"
echo $gstreamer_dir
if [ -z "${gstreamer_dir}" ];then
    echo "\nERROR : lib32-gstreamer1.0 directory not found\n"
    exit
fi
cd $gstreamer_dir
gstreamer_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${gstreamer_package_dir} ];then
    echo "\nERROR : gstreamer1.0 package not found\n"
    exit
fi
cd $gstreamer_package_dir
tar -cjf gstreamer.tgz *
mv gstreamer.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained gstreamer-1.0 package successfully\n"

#Acquire gstreamer plugins base package
cd $BUILD_DIR
echo "\nAcquiring gstreamer1.0-plugins-base package"
gstreamer_plugins_base_dir="$(find . -maxdepth 2 -type d -name *gstreamer1.0-plugins-base | grep -v nativesdk)"
echo $gstreamer_plugins_base_dir
if [ -z "${gstreamer_plugins_base_dir}" ];then
    echo "\nERROR : lib32-gstreamer1.0-plugins-base directory not found\n"
    exit
fi
cd $gstreamer_plugins_base_dir
gstreamer_plugins_base_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${gstreamer_plugins_base_package_dir} ];then
    echo "\nERROR : gstreamer1.0-plugins-base package not found\n"
    exit
fi
cd $gstreamer_plugins_base_package_dir
tar -cjf gstreamer_plugins_base.tgz *
mv gstreamer_plugins_base.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained gstreamer1.0-plugins-base package successfully\n"

#Acquire glib-2.0 package
cd $BUILD_DIR
echo "\nAcquiring glib-2.0 package"
glib_2_0_dir="$(find . -maxdepth 2 -type d -name *glib-2.0 | grep -v nativesdk)"
# Prefer lib32 if present
glib_2_0_dir=$(echo "$glib_2_0_dir" | grep lib32 || echo "$glib_2_0_dir" | head -n1)
echo $glib_2_0_dir
if [ -z "${glib_2_0_dir}" ];then
    echo "\nERROR : lib32-glib-2.0 directory not found\n"
    exit
fi
cd $glib_2_0_dir
glib_2_0_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${glib_2_0_package_dir} ];then
    echo "\nERROR : glib-2.0 package not found\n"
    exit
fi
cd $glib_2_0_package_dir
tar -cjf glib2.0.tgz *
mv glib2.0.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained glib-2.0 package successfully\n"

#Acquire libffi package
cd $BUILD_DIR
echo "\nAcquiring libffi package"
libffi_dir="$(find . -maxdepth 2 -type d -name *libffi | grep -v nativesdk)"
# Prefer lib32 if present
libffi_dir=$(echo "$libffi_dir" | grep lib32 || echo "$libffi_dir" | head -n1)
echo $libffi_dir
if [ -z "${libffi_dir}" ];then
    echo "\nERROR : lib32-libffi directory not found\n"
    exit
fi
cd $libffi_dir
libffi_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${libffi_package_dir} ];then
    echo "\nERROR : libffi package not found\n"
    exit
fi
cd $libffi_package_dir
tar -cjf libffi.tgz *
mv libffi.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained libffi package successfully\n"

#Acquire wayland package
cd $BUILD_DIR
echo "\nAcquiring wayland package"
wayland_dir="$(find . -maxdepth 2 -type d -name *wayland | grep -v nativesdk)"
# Prefer lib32 if present
wayland_dir=$(echo "$wayland_dir" | grep lib32 || echo "$wayland_dir" | head -n1)
echo $wayland_dir
if [ -z "${wayland_dir}" ];then
    echo "\nERROR : lib32-wayland directory not found\n"
    exit
fi
cd $wayland_dir
wayland_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${wayland_package_dir} ];then
    echo "\nERROR : wayland package not found\n"
    exit
fi
cd $wayland_package_dir
tar -cjf wayland.tgz *
mv wayland.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained wayland package successfully\n"

#Acquire vulkan-loader package
cd $BUILD_DIR
echo "\nAcquiring vulkan-loader package"
vulkan_loader_dir="$(find . -maxdepth 2 -type d -name *vulkan-loader | grep -v nativesdk)"
echo $vulkan_loader_dir
if [ -z "${vulkan_loader_dir}" ];then
    echo "\nERROR : lib32-vulkan-loader directory not found\n"
    exit
fi
cd $vulkan_loader_dir
vulkan_loader_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${vulkan_loader_package_dir} ];then
    echo "\nERROR : vulkan-loader package not found\n"
    exit
fi
cd $vulkan_loader_package_dir
tar -cjf vulkan_loader.tgz *
mv vulkan_loader.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained vulkan-loader package successfully\n"

#Acquire wayland-protocols package
cd $BUILD_DIR
echo "\nAcquiring wayland-protocols package"
wayland_protocols_dir="$(find . -maxdepth 2 -type d -name *wayland-protocols | grep -v nativesdk)"
echo $wayland_protocols_dir
if [ -z "${wayland_protocols_dir}" ];then
    echo "\nERROR : lib32-wayland-protocols directory not found\n"
    exit
fi
cd $wayland_protocols_dir
wayland_protocols_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${wayland_protocols_package_dir} ];then
    echo "\nERROR : wayland_protocols package not found\n"
    exit
fi
cd $wayland_protocols_package_dir
tar -cjf wayland_protocols.tgz *
mv wayland_protocols.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained wayland protocols package successfully\n"

#Acquire glm package
cd $BUILD_DIR
echo "\nAcquiring glm package"
glm_dir="$(find . -maxdepth 2 -type d -name *glm | grep -v nativesdk)"
echo $glm_dir
if [ -z "${glm_dir}" ];then
    echo "\nERROR : lib32-glm directory not found\n"
    exit
fi
cd $glm_dir
glm_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${glm_package_dir} ];then
    echo "\nERROR : glm package not found\n"
    exit
fi
cd $glm_package_dir
tar -cjf glm.tgz *
mv glm.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained glm package successfully\n"

#Acquire vulkan-loader package
cd $BUILD_DIR
echo "\nAcquiring vulkan-loader package"
vulkan_loader_dir="$(find . -maxdepth 2 -type d -name *vulkan-loader | grep -v nativesdk)"
echo $vulkan_loader_dir
if [ -z "${vulkan_loader_dir}" ];then
    echo "\nERROR : lib32-vulkan-loader directory not found\n"
    exit
fi
cd $vulkan_loader_dir
vulkan_loader_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${vulkan_loader_package_dir} ];then
    echo "\nERROR : vulkan-loader package not found\n"
    exit
fi
cd $vulkan_loader_package_dir
tar -cjf vulkan_loader.tgz *
mv vulkan_loader.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained vulkan-loader package successfully\n"

#Acquire wayland-protocols package
cd $BUILD_DIR
echo "\nAcquiring wayland-protocols package"
wayland_protocols_dir="$(find . -maxdepth 2 -type d -name *wayland-protocols | grep -v nativesdk)"
echo $wayland_protocols_dir
if [ -z "${wayland_protocols_dir}" ];then
    echo "\nERROR : lib32-wayland-protocols directory not found\n"
    exit
fi
cd $wayland_protocols_dir
wayland_protocols_package_dir="$(find . -maxdepth 2 -type d -name image)"
if [ -z ${wayland_protocols_package_dir} ];then
    echo "\nERROR : wayland-protocols package not found\n"
    exit
fi
cd $wayland_protocols_package_dir
tar -cjf wayland_protocols.tgz *
mv wayland_protocols.tgz $ROOT_DIR/Packages
echo "SUCCESS : Obtained wayland-protocols package successfully\n"

#Additionial libs
cd $BUILD_DIR/${gstreamer_plugins_base_dir}
sysroot_dir="$(find .  -type d -name lib32-recipe-sysroot)"
cd $sysroot_dir
lib_dir="$(dirname "$(find .  -type f -name libpcre* | head -n 1)")"
cd $lib_dir
mkdir -p $BUILD_DIR/${gstreamer_plugins_base_dir}/additionial_libs/usr/lib/
cp libpcre* $BUILD_DIR/${gstreamer_plugins_base_dir}/additionial_libs/usr/lib
cp liborc* $BUILD_DIR/${gstreamer_plugins_base_dir}/additionial_libs/usr/lib
cd $BUILD_DIR/${gstreamer_plugins_base_dir}
lib_dir2="$(dirname "$(find . -type f -name libz*| head -n 1)")"
cd $lib_dir2
mkdir -p $BUILD_DIR/${gstreamer_plugins_base_dir}/additionial_libs/lib/
cp libz* $BUILD_DIR/${gstreamer_plugins_base_dir}/additionial_libs/lib
cd $BUILD_DIR/${gstreamer_plugins_base_dir}/
tar -cjf additionial_libs.tgz additionial_libs
cp additionial_libs.tgz $ROOT_DIR/Packages
rm -rf additionial_libs*


cd $ROOT_DIR
tar -cjf Packages.tgz Packages/
echo "SUCCESS : Created Packages.tgz Successfully in $ROOT_DIR"
