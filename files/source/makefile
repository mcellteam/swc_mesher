# Simply provide a means of copying from git working directory to Blender addon directory

# Linux:
INSTALL_DIR = ~/.config/blender/2.78/scripts/addons/

# Mac:
#INSTALL_DIR = ~/Library/Application\ Support/Blender/2.74/scripts/addons/

install:
	@if [ "$(INSTALL_DIR)" ]; then \
	  cp -v swc_mesher.py $(INSTALL_DIR); \
	fi
	@echo Done

