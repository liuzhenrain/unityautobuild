# !/usr/local/bin/python
# -*- coding=utf8 -*-

import os
import subprocess
import sys
import tail
import thread
import time
import copy
import shutil


class ExportProj:
    _sourcePath = ""
    _jsonobj = None
    _platform = ""
    _pack_games = []
    _open_log = False
    _unity_path = ""

    def __init__(self, path, jsonobj):
        self._sourcePath = path
        self._jsonobj = jsonobj
        self._logpath = self._sourcePath + os.sep + "exportlog.log"
        self._batchcmd = [self._jsonobj["unity_path"], '-batchmode', '-projectPath',
                          self._sourcePath,
                          '-executeMethod', "CommandTool.GenWrapFiles",
                          '-logFile', self._logpath, '-quit', "-nographics"]

    def _unity_log_tail(self, txt):
        # log = txt.split("\n")
        print("Print Log:" + txt)

    def _tail_thread(self, tail_file):
        print "wait for tail file ... %s" % tail_file

        while True:
            if os.path.exists(tail_file):
                print "Start tail file..... %s" % tail_file
                break

        t = tail.Tail(tail_file)
        t.register_callback(self._unity_log_tail)
        t.follow(s=0.1)

    def _genWrapFiles(self):
        print "Start reBuild Wrap Files"
        if os.path.exists(self._logpath):
            os.remove(self._logpath)
        print self._batchcmd

        # new thread to tail log file
        # thread.start_new_thread(self._tail_thread, (self._logpath,))

        os.system(" ".join(self._batchcmd))
        # process = subprocess.Popen(self._batchcmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=self._sourcePath)
        time.sleep(5)
        print "Gen wrap files all"
        self._batchcmd[5] = "CommandTool.GenWrapAll"

        os.system(" ".join(self._batchcmd))

        print "Build Wrap Files Complete"

    def _buildGameAssets(self, key):
        print "Start Build %s Assets" % key
        self._batchcmd[5] = "CommandTool.BuildAssets"
        if os.path.exists(self._logpath):
            os.remove(self._logpath)
        batchcmd = copy.deepcopy(self._batchcmd)
        batchcmd.append("-platform ios -name %s" % key)
        # thread.start_new_thread(self._tail_thread, (self._logpath,))
        os.system(" ".join(batchcmd))
        # process = subprocess.Popen(batchcmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=self._sourcePath)
        print "%s Building Complete" % key

    def genProject(self):
        print "Build Asssetbundle Starting..."
        if not self._jsonobj["skip_confuse"]:
            self._genWrapFiles()
            time.sleep(5)
        self._buildGameAssets("Main")
        time.sleep(5)
        for key in self._jsonobj["pack_game"]:
            self._buildGameAssets(key)
            time.sleep(5)
        time.sleep(5)
        print "Export XCodeProject Starting...", self._sourcePath
        assetPath = os.path.join(self._sourcePath, "Assets")
        os.chdir(assetPath)
        os.system("mkdir %s/StreamingAssets" % assetPath)
        os.system("mv Res_* StreamingAssets")
        os.chdir(assetPath + os.sep + "StreamingAssets")
        os.system("find . -name '*.zip' -exec tar xf {} \\; -print")
        os.system("rm -f Res_*")
        batchcmd = copy.deepcopy(self._batchcmd)
        batchcmd[5] = "CommandTool.BuildXCode"
        os.chdir(self._sourcePath)
        basename = os.path.basename(self._sourcePath)
        xcodepathparent = os.path.abspath(os.path.dirname(self._sourcePath))
        xcodepath = os.path.join(xcodepathparent, basename + "_XCode")
        if os.path.exists(xcodepath):
            print "Has exist xcode folder will be REMOVED."
            shutil.rmtree(xcodepath)
        print "Create XCodeProject Folder:", xcodepath
        os.mkdir(xcodepath)
        smallgames = "_".join(self._jsonobj["pack_game"])
        print "XcodePath", xcodepath, "SmallGames", smallgames
        batchcmd.append("-xcodepath %s -smallgames %s" % (xcodepath, smallgames))
        os.system(" ".join(batchcmd))
        print "Export XCodeProject Complete"
