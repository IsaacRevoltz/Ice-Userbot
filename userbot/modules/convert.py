# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the  GPL-3.0 License;
# you may not use this file except in compliance with the License.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#

import asyncio
import io
import os

from PIL import Image

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP
from userbot.utils import edit_delete, edit_or_reply, ice_cmd, runcmd


@@ -26,23 +26,23 @@ async def cevir(event):
        if len(botice) < 1:
            await edit_delete(
                event,
                "**Comando desconhecido! digite** .help convert **se precisar de ajuda**",
                30,
            )
            return
    except BaseException:
        await edit_delete(
            event,
            "**Comando desconhecido! digite** .help convert **se precisar de ajuda**",
            30,
        )
        return
    if botice in ["foto", "photo"]:
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.sticker:
            await edit_delete(event, "**Por favor, responda ao adesivo.**")
            return
        xxnx = await edit_or_reply(event, "Converter em foto...")
        foto = io.BytesIO()
        foto = await event.client.download_media(rep_msg.sticker, foto)
        im = Image.open(foto).convert("RGB")
@@ -55,18 +55,18 @@ async def cevir(event):
        await xxnx.delete()
        os.remove("sticker.png")
    elif botice in ["sound", "audio"]:
        EFEKTLER = ["tosse", "robo", "jedi", "rapido", "eco"]
        efekt = event.pattern_match.group(2)
        if len(efekt) < 1:
            return await edit_delete(
                event,
                "**O efeito que você especificou não foi encontrado!**\n**Efeitos que você pode usar:** tosse/robo/jedi/rapido/eco`",
                30,
            )
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not (rep_msg.voice or rep_msg.audio):
            return await edit_delete(event, "**Por favor, responda ao arquivo de áudio.**")
        xxx = await edit_or_reply(event, "Aplicando o efeito...")
        if efekt in EFEKTLER:
            indir = await rep_msg.download_media()
            KOMUT = {
@@ -91,13 +91,13 @@ async def cevir(event):
            os.remove("output.mp3")
        else:
            await xxx.edit(
                "**O efeito que você especificou não foi encontrado!**\n**Efeitos que você pode usar:** tosse/robo/jedi/rapido/eco`"
            )
    elif botice == "mp3":
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.video:
            return await edit_delete(event, "**Por favor, responda ao vídeo!**")
        xx = await edit_or_reply(event, "Converter em som...")
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg.video)
        gif = await asyncio.create_subprocess_shell(
@@ -114,25 +114,25 @@ async def cevir(event):
            )
        except BaseException:
            os.remove(video)
            return await xx.edit("**Não é possível converter para áudio! 🥺**")
        await xx.delete()
        os.remove("out.mp3")
        os.remove(video)
    else:
        await xx.edit(
            "**Comando desconhecido! digite** .help convert **se precisar de ajuda**"
        )