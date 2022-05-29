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


@ice_cmd(pattern="convert ?(foto|audio|gif|voice|photo|mp3)? ?(.*)")
async def cevir(event):
    botice = event.pattern_match.group(1)
    try:
        if len(botice) < 1:
            await edit_delete(
                event,
                "**Comando desconhecido! digite** `.help convert` **se precisar de ajuda**",
                30,
            )
            return
    except BaseException:
        await edit_delete(
            event,
            "**Comando desconhecido! digite** `.help convert` **se precisar de ajuda**",
            30,
        )
        return
    if botice in ["foto", "photo"]:
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.sticker:
            await edit_delete(event, "**Por favor, responda ao adesivo.**")
            return
        xxnx = await edit_or_reply(event, "`Converter em foto...`")
        foto = io.BytesIO()
        foto = await event.client.download_media(rep_msg.sticker, foto)
        im = Image.open(foto).convert("RGB")
        im.save("sticker.png", "png")
        await event.client.send_file(
            event.chat_id,
            "sticker.png",
            reply_to=rep_msg,
        )
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
        xxx = await edit_or_reply(event, "`Aplicando o efeito...`")
        if efekt in EFEKTLER:
            indir = await rep_msg.download_media()
            KOMUT = {
                "bengek": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
            }
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {KOMUT[efekt]} output.mp3"
            )
            await ses.communicate()
            await event.client.send_file(
                event.chat_id,
                "output.mp3",
                thumb="userbot/resources/logo.jpg",
                reply_to=rep_msg,
            )
            await xxx.delete()
            os.remove(indir)
            os.remove("output.mp3")
        else:
            await xxx.edit(
                "**O efeito que você especificou não foi encontrado!**\n**Efeitos que você pode usar:** tosse/robo/jedi/rapido/eco`"
            )
    elif botice == "mp3":
        rep_msg = await event.get_reply_message()
        if not event.is_reply or not rep_msg.video:
            return await edit_delete(event, "**Por favor, responda ao vídeo!**")
        xx = await edit_or_reply(event, "`Converter em som...`")
        video = io.BytesIO()
        video = await event.client.download_media(rep_msg.video)
        gif = await asyncio.create_subprocess_shell(
            f"ffmpeg -y -i '{video}' -vn -b:a 128k -c:a libmp3lame out.mp3"
        )
        await gif.communicate()
        await xx.edit("`Uploading Sound...`")
        try:
            await event.client.send_file(
                event.chat_id,
                "out.mp3",
                thumb="userbot/resources/logo.jpg",
                reply_to=rep_msg,
            )
        except BaseException:
            os.remove(video)
            return await xx.edit("**Não é possível converter para áudio! 🥺**")
        await xx.delete()
        os.remove("out.mp3")
        os.remove(video)
    else:
        await xx.edit(
            "**Comando desconhecido! digite** `.help convert` **se precisar de ajuda**"
        )
        return


@ice_cmd(pattern="makevoice$")
async def makevoice(event):
    if not event.reply_to:
        return await edit_delete(event, "**Por favor, responda ao áudio ou vídeo**")
    msg = await event.get_reply_message()
    if not event.is_reply or not (msg.audio or msg.video):
        return await edit_delete(event, "**Por favor, responda ao áudio ou vídeo**")
    xxnx = await edit_or_reply(event, "`Processando...`")
    dl = msg.file.name
    file = await msg.download_media(dl)
    await xxnx.edit("`Converting to Voice Note...`")
    await runcmd(
        f"ffmpeg -i '{file}' -map 0:a -codec:a libopus -b:a 100k -vbr on man.opus"
    )
    await event.client.send_message(
        event.chat_id, file="man.opus", force_document=False, reply_to=msg
    )
    await xxnx.delete()
    os.remove(file)
    os.remove("man.opus")


CMD_HELP.update(
    {
        "convert": f"**Plugin : **`core`\
        \n\n  •  **Syntax :** `{cmd}converter foto`\
        \n  •  **Function : **Para converter adesivo em foto\
        \n\n  •  **Syntax :** `{cmd}converter mp3`\
        \n  •  **Function : **Para converter de vídeo para arquivo mp3\
        \n\n  •  **Syntax :** `{cmd}makevoice`\
        \n  •  **Function : **Para converter áudio em nota de voz\
        \n\n  •  **Syntax :** `{cmd}converter audio` <efeito>\
        \n  •  **Function : **Para adicionar um efeito de som fino\
        \n  •  **List Efek :** `tosse`, `jedi`, `eco`, `robo`\
    "
    }
)
