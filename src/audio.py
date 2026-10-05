# coding=utf-8
'''
(C) Copyright 2021 Steven;
@author: Steven kangweibaby@163.com
(C) Copyright 2026 Zhang-ikun;
@maintainer: Zhang-ikun 2439884871@qq.com
@date: 2021-05-31

使用 pygame 播放音频

'''

import pygame

from chess import Chess
from logger import logger

import system

dirpath = system.get_dirpath()

AUDIO_MOVE = str(dirpath / 'audios/move.wav')
AUDIO_CAPTURE = str(dirpath / 'audios/capture.wav')
AUDIO_CHECK = str(dirpath / 'audios/check.wav')
AUDIO_INVALID = str(dirpath / 'audios/invalid.wav')
AUDIO_NEW_GAME = str(dirpath / 'audios/newgame.wav')


ready = False
sounds = {}


def init():
    global ready
    try:
        pygame.mixer.init()
        ready = True
    except Exception as e:
        logger.warning("audio init failed: %s", e)


def play(audio_type):
    if not ready:
        return

    if audio_type == Chess.CAPTURE:
        audio = AUDIO_CAPTURE
    elif audio_type == Chess.MOVE:
        audio = AUDIO_MOVE
    elif audio_type == Chess.CHECK:
        audio = AUDIO_CHECK
    elif audio_type == Chess.INVALID:
        audio = AUDIO_INVALID
    elif audio_type == Chess.NEWGAME:
        audio = AUDIO_NEW_GAME
    elif audio_type == Chess.CHECKMATE:
        audio = AUDIO_CHECK
    else:
        return

    sound = sounds.get(audio)
    if sound is None:
        try:
            sound = pygame.mixer.Sound(audio)
        except Exception as e:
            logger.warning("load audio failed %s: %s", audio, e)
            return
        sounds[audio] = sound

    logger.info("play audio %s", audio)
    sound.play()
