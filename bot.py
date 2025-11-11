import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import unicodedata
from discord import app_commands
import json
import asyncio
import aiohttp
from typing import Optional, Dict, List
import logging
import requests
import uuid
from datetime import datetime
from datetime import timedelta
from discord.ui import Button, View, Modal, TextInput


# Configurar logging para mejor control
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')

print("Starting Yuki Bot...")

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv('TOKEN')
if not TOKEN:
	print("ERROR: No se encontró la variable TOKEN en .env")
	exit()

# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot
bot = commands.Bot(
	command_prefix='!', 
	intents=intents, 
	help_command=None,
	max_messages=1000  #cache de mensajes
)

# ============ CONFIGURACIONES GLOBALES ============
CONFIG = {
	'welcome_channel': 1429650615205756938,
	'music_voice_channel': 1429910096401662164,
	'music_text_channel': 1429910096401662164,
	'event_channel_single': 1428587161757679666,
	'event_channel_list': 1428471960438046910,
	'guide_channel': 1429889947892060180
}

# ============ SISTEMA DE NORMALIZACIÓN ============
def normalizar_comando(texto: str) -> str:
	"""Función optimizada para normalización de comandos"""
	if not texto.startswith('!'):
		return texto
	
	texto = texto.lower().strip()
	texto = unicodedata.normalize("NFD", texto)
	texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
	
	# Preservar menciones y espacios importantes
	texto = texto.replace("! ", "!").replace(" !","!")
	return ' '.join(texto.split())

# ============ EVENTOS PRINCIPALES ============
@bot.event
async def on_ready():
	
	print(f'✅ {bot.user} conectado exitosamente!')
	
	try:
		synced = await bot.tree.sync()
		print(f'✅ {len(synced)} comandos sincronizados')
	except Exception as e:
		print(f'❌ Error sincronizando comandos: {e}')

@bot.event
async def on_member_join(member):
	channel = member.guild.get_channel(CONFIG['welcome_channel'])
	if channel:
		mensajes = [
			f"¡Hola {member.mention}! 🌸 Bienvenido/a a **{member.guild.name}** 💖",
			f"¡Bienvenid@ {member.mention}! 🎮 Espero que pases buenos momentos en **{member.guild.name}**",
			f"¡Hey {member.mention}! 🌟 Te damos la bienvenida a **{member.guild.name}**"
		]
		
		embed = discord.Embed(
			title="🎉 ¡Nuevo miembro!",
			description=random.choice(mensajes),
			color=discord.Color.pink()
		)
		embed.add_field(
			name="💫 Comandos útiles",
			value="Usa `!comandos` para ver lo que puedo hacer",
			inline=False
		)
		embed.set_thumbnail(url=member.display_avatar.url)
		
		await channel.send(embed=embed)

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	
	# Solo procesar si es un comando
	if message.content.startswith('!'):
		message.content = normalizar_comando(message.content)
		await bot.process_commands(message)

# ============ COMANDOS DE TEXTO OPTIMIZADOS ============
@bot.command(name='ayuda')
async def ayuda(ctx):
	respuestas = [
		"Q te pasa we?",
		"¿Necesitas ayuda? ¡Usa `!comandos`!"
	]
	await ctx.send(random.choice(respuestas))

@bot.command(name='besame')
async def besame(ctx):
	"""Comando besame fusionado con besaa"""
	await ctx.invoke(bot.get_command('besaa'), usuario=ctx.author)

@bot.command(name='200')
async def status(ctx):
	"""Verificación de estado mejorada"""
	embed = discord.Embed(
		title="Estado del Servidor",
		description="**Status: 200 OK** 🟢",
		color=discord.Color.green()
	)
	embed.add_field(name="Latencia", value=f"{round(bot.latency * 1000)}ms", inline=True)
	await ctx.send(embed=embed)
	
@bot.command(name='besaa')
async def besaa(ctx, usuario: discord.Member = None):
	"""Comando de beso optimizado y unificado"""
	if usuario is None:
		await ctx.send("❌ Debes mencionar a alguien: `!besaa @usuario`")
		return
	
	if usuario == ctx.author:
		respuestas = [
			"¿Quieres besarte a ti mismo?",
			"Primero un cafecito, ¿no?",
			"Eso es un poco raro..."
		]
		await ctx.send(random.choice(respuestas))
		return

	respuestas = [
		f"\\*besa a {usuario.mention}\\* y luego sigue con su vida tranquila...",
		f"\\*besa a {usuario.mention}\\* y se queda sonriendo...",
		f"¡Wow!\\n\\*besa a {usuario.mention}\\* y desaparece misteriosamente 🌼",
		f"¡Momento épico!\\n\\*besa a {usuario.mention}\\* y continúa su aventura ⚔️",
		f"\\*besa a {usuario.mention}\\*",
		f"¡Sorpresa!\\n\\*besa a {usuario.mention}\\* y todos... \\n se quedan en silencio xd 🤫",
		f"\\*besa a {usuario.mention}\\* y sonríe tímidamente... 😳",
		f"En secreto\\n\\*besa a {usuario.mention}\\* y se escabulle sin que nadie lo note 🕵️",
		f"Con estilo \\n \\*besa a {usuario.mention}\\* y hace una reverencia 🎩",
		f"\\*besa a {usuario.mention}\\* y luego se aleja lentamente… 🌸"
	]
	
	await ctx.send(random.choice(respuestas))

@bot.command(name='info')
async def info(ctx):
	mensajes = [
		f"¡Hola {ctx.author.mention}! 🌸 Soy **Yuki**, tu bot amigable 💖",
		f"¡Hey {ctx.author.mention}! 🌷 Soy **Yuki** 💜",
		f"¡Hola {ctx.author.mention}! 🌟 Soy **Yuki**, tu compañera virtual 💖",
		f"¡Qué alegría verte {ctx.author.mention}! 🌸",
		f"¡Hola {ctx.author.mention}! 🌺 Soy **Yuki** 💖"
	]
	
	embed = discord.Embed(
		title="🌸 Información de Yuki",
		description=random.choice(mensajes),
		color=discord.Color.pink()
	)
	embed.add_field(
		name="🎯 Mi propósito",
		value="Estoy aquí para ayudarte, responder tus dudas y alegrarte el día",
		inline=False
	)
	embed.add_field(
		name="💫 Comandos disponibles",
		value="Usa `!comandos` para ver todo lo que puedo hacer",
		inline=False
	)
	embed.set_thumbnail(url=bot.user.display_avatar.url)
	
	await ctx.send(embed=embed)

@bot.command(name='hola')
async def hola(ctx):
	saludos = [
		f"Hey {ctx.author.mention}, ¿qué tal? ❤️❤️",
		f"¡Hola {ctx.author.mention}! 👋",
		f"¡Qué onda {ctx.author.mention}!",
		f"¡Ey {ctx.author.mention}! ¿Cómo va todo?",
		f"¡Saludos {ctx.author.mention}!",
		f"¡Qué pasa {ctx.author.mention}!, ¿ya comiste?",
		f"¡Hey {ctx.author.mention}, listo para jugar? 🎮🔥",
		f"¡Hola {ctx.author.mention}! Espero que estés teniendo un gran día ✨✨",
		f"¡Ey {ctx.author.mention}! ¿Listo para la aventura?",
		f"¡Qué onda {ctx.author.mention}! Vamos a divertirnos, ¿que quieres hacer hoy?",
		f"¡Hola {ctx.author.mention}! Mantén la calma y juega tranquilo"
	]
	
	embed = discord.Embed(
		description=random.choice(saludos),
		color=discord.Color.blue()
	)
	await ctx.send(embed=embed)

@bot.command(name='qhago')
async def qhago(ctx):
	respuesta = random.choice([
		"no sé we. ¿por qué me preguntas a mi?",
		"¿Yo qué sé? Pregúntale a Google",
		"Mmm... mejor pregúntale a alguien más"
	])
	await ctx.send(f"{respuesta} <:mmm:1429328016307130378>")

# ============ SISTEMA DE MÚSICA ============

class MusicSystem:
    """Sistema de música optimizado y corregido"""
    
    def __init__(self):
        self.queues: Dict[int, List[str]] = {}
        self.current: Dict[int, str] = {}
        self.requests: Dict[int, List[discord.Member]] = {}
        self._event_loops: Dict[int, asyncio.AbstractEventLoop] = {}
    
    def check_voice_channel(self, interaction: discord.Interaction) -> tuple[bool, str]:
        """Verificar canal de voz permitido"""
        user_vc = interaction.user.voice
        
        if not user_vc or not user_vc.channel:
            return False, f"Debes estar conectado al canal de voz <#{CONFIG['music_voice_channel']}>"
        
        if user_vc.channel.id != CONFIG['music_voice_channel']:
            return False, f"❌ Solo puedes usar este comando en <#{CONFIG['music_voice_channel']}>"
        
        if user_vc.self_deaf or user_vc.self_mute:
            return False, "❌ Debes estar en modo de escucha (no silenciado)"
        
        return True, "OK"
    
    def check_bot_in_allowed_channel(self, interaction):
        """Verifica que el bot esté en el canal de voz permitido"""
        vc = interaction.guild.voice_client
        
        if vc and vc.channel.id != CONFIG['music_voice_channel']:
            return False, f"Solo puedes usar este comando en: <#{CONFIG['music_voice_channel']}>."
        
        return True, "OK"
    
    async def send_music_embed(self, guild: discord.Guild, embed: discord.Embed = None, **kwargs):
        """Enviar embed al canal de música"""
        try:
            channel = guild.get_channel(CONFIG['music_text_channel'])
            if channel:
                if embed is None:
                    embed = discord.Embed(**kwargs)
                await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error enviando embed de música: {e}")
    
    def _get_or_create_loop(self, guild_id: int):
        """Obtener o crear event loop para un guild específico"""
        if guild_id not in self._event_loops:
            self._event_loops[guild_id] = asyncio.get_event_loop()
        return self._event_loops[guild_id]
    
    async def play_next(self, guild_id: int, vc: discord.VoiceClient):
        try:
            # Verificar si todavía estamos conectados
            if not vc or not vc.is_connected():
                return
            
            if not self.queues.get(guild_id):
                # Esperar antes de desconectar
                await asyncio.sleep(30)
                
                # Verificar nuevamente antes de desconectar
                if vc and vc.is_connected() and not vc.is_playing():
                    await self.send_music_embed(
                        vc.guild,
                        title="🎵 Desconexión Automática",
                        description="No hay más canciones en la lista. Me desconecto! 👋",
                        color=0xe74c3c
                    )
                    await vc.disconnect()
                    
                    # Limpiar datos del guild
                    if guild_id in self.queues:
                        del self.queues[guild_id]
                    if guild_id in self.current:
                        del self.current[guild_id]
                    if guild_id in self.requests:
                        del self.requests[guild_id]
                return
            
            current_song = self.queues[guild_id].pop(0)
            current_requester = self.requests[guild_id].pop(0)
            self.current[guild_id] = current_song
            
            ruta = f"./songs/{current_song}.mp3"
            
            if not os.path.exists(ruta):
                logger.warning(f"Archivo no encontrado: {ruta}")
                # Intentar con la siguiente canción
                await self.play_next(guild_id, vc)
                return
            
            def after_play(error):
                """Callback después de la reproducción - CORREGIDO"""
                if error:
                    logger.error(f"Error en reproducción: {error}")
                
                # Usar el event loop específico del guild
                loop = self._get_or_create_loop(guild_id)
                
                # Crear task de forma segura
                if loop.is_running():
                    asyncio.run_coroutine_threadsafe(
                        self._safe_play_next(guild_id, vc), 
                        loop
                    )
                else:
                    # Si el loop no está corriendo, usar el loop por defecto
                    asyncio.create_task(self._safe_play_next(guild_id, vc))
            
            # Reproducir la canción
            vc.play(discord.FFmpegPCMAudio(ruta), after=after_play)
            
            # Embed de canción actual
            next_songs = self.queues[guild_id][:3]
            next_text = "\n".join([
                f"{i+1}. `{song}` - {self.requests[guild_id][i].mention}" 
                for i, song in enumerate(next_songs)
            ]) if next_songs else "No hay más canciones en cola"
            
            embed = discord.Embed(
                title="🎵 Reproduciendo Ahora",
                color=0x2ecc71
            )
            embed.add_field(
                name="Canción actual:",
                value=f"`{current_song}`",
                inline=False
            )
            embed.add_field(
                name="Solicitada por:",
                value=current_requester.mention,
                inline=False
            )
            embed.add_field(
                name="Próximas canciones:",
                value=next_text,
                inline=False
            )
            
            await self.send_music_embed(vc.guild, embed=embed)
            
        except Exception as e:
            logger.error(f"Error en play_next: {e}")
            # Reintentar después de un breve delay
            await asyncio.sleep(2)
            await self._safe_play_next(guild_id, vc)
    
    async def _safe_play_next(self, guild_id: int, vc: discord.VoiceClient):
        try:
            await self.play_next(guild_id, vc)
        except Exception as e:
            logger.error(f"Error en _safe_play_next: {e}")
            # Si hay error crítico, desconectar
            try:
                if vc and vc.is_connected():
                    await vc.disconnect()
            except Exception as disconnect_error:
                logger.error(f"Error desconectando: {disconnect_error}")
    
    async def cleanup_guild(self, guild_id: int):
        """Limpiar recursos de un guild específico"""
        try:
            if guild_id in self.queues:
                del self.queues[guild_id]
            if guild_id in self.current:
                del self.current[guild_id]
            if guild_id in self.requests:
                del self.requests[guild_id]
            if guild_id in self._event_loops:
                del self._event_loops[guild_id]
        except Exception as e:
            logger.error(f"Error limpiando guild {guild_id}: {e}")

# Instancia del sistema de música
music_system = MusicSystem()

# ============ COMANDOS DE MÚSICA ============
@bot.tree.command(name="play", description="Sistema de música - Reproduce canciones")
@app_commands.describe(
    action="Qué quieres hacer"
)
@app_commands.choices(action=[
    app_commands.Choice(name="🎵 Reproducir canción", value="play"),
    app_commands.Choice(name="⏸️ Pausar/Reanudar", value="pause"),
    app_commands.Choice(name="⏭️ Saltar canción", value="skip"),
    app_commands.Choice(name="📋 Ver cola actual", value="queue"),
    app_commands.Choice(name="🚪 Salir del canal", value="leave"),
    app_commands.Choice(name="🎶 Lista de canciones", value="list")
])
async def play(interaction: discord.Interaction, action: app_commands.Choice[str]):
    
    
    action_value = action.value
    
    # Si elige listar canciones
    if action_value == "list":
        canciones_disponibles = obtener_lista_canciones()
        
        if not canciones_disponibles:
            embed = discord.Embed(
                title="🎵 Lista de Canciones",
                description="No hay canciones disponibles en la biblioteca.",
                color=0xe74c3c
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Crear lista formateada de canciones
        lista_canciones = "\n".join([f"🎵 `{cancion}`" for cancion in canciones_disponibles])
        
        embed = discord.Embed(
            title="🎵 Biblioteca de Canciones Disponibles",
            description=(
                f"**Total de canciones:** {len(canciones_disponibles)}\n\n"
                f"{lista_canciones}\n\n"
                "**Cómo reproducir:**\n"
                "Selecciona **🎵 Reproducir canción** y escribe el nombre exacto\n"
                "*O usa los botones de abajo para seleccionar rápido*"
            ),
            color=0x3498db
        )
        
        # Crear botones para selección rápida (máximo 5 canciones)
        view = View()
        for i, cancion in enumerate(canciones_disponibles[:5]):
            button = Button(
                label=cancion[:25] + ("..." if len(cancion) > 25 else ""),
                style=discord.ButtonStyle.secondary,
                custom_id=f"play_{cancion}"
            )
            
            async def button_callback(interaction_btn, cancion_btn=cancion):
                await play_selected_song(interaction_btn, cancion_btn)
            
            button.callback = button_callback
            view.add_item(button)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        return
    
    # Para acciones que no requieren canción
    try:
        if action_value == "play":
            # Para "reproducir", enviar mensaje instructivo
            canciones_disponibles = obtener_lista_canciones()
            
            if not canciones_disponibles:
                await interaction.response.send_message(
                    "❌ No hay canciones disponibles en la biblioteca.",
                    ephemeral=True
                )
                return
            
            # Crear lista de opciones para el select menu
            options = []
            for cancion in canciones_disponibles[:25]:
                options.append(discord.SelectOption(
                    label=cancion[:100],
                    value=cancion,
                    description=cancion[:50] + ("..." if len(cancion) > 50 else "")
                ))
            
            # Crear el select menu
            select = discord.ui.Select(
                placeholder="🎵 Selecciona una canción...",
                options=options
            )
            
            async def select_callback(select_interaction):
                if select_interaction.user.id != interaction.user.id:
                    await select_interaction.response.send_message(
                        "❌ Este menú no es para ti.", 
                        ephemeral=True
                    )
                    return
                
                cancion_seleccionada = select.values[0]
                await play_selected_song(select_interaction, cancion_seleccionada)
            
            select.callback = select_callback
            
            view = View()
            view.add_item(select)
            
            embed = discord.Embed(
                title="🎵 Selecciona una Canción",
                description=(
                    f"**{len(canciones_disponibles)}** canciones disponibles\n\n"
                    "Selecciona una canción del menú desplegable 👇\n"
                    "O usa `/play action: \"🎶 Lista de canciones\"` para ver la lista completa"
                ),
                color=0x3498db
            )
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            
        elif action_value == "pause":
            await pause(interaction)
            
        elif action_value == "skip":
            await skip(interaction)
            
        elif action_value == "queue":
            await queue(interaction)
            
        elif action_value == "leave":
            await leave(interaction)

    except Exception as e:
        logger.error(f"Error en comando play: {e}")
        await interaction.response.send_message(
            "❌ Ocurrió un error al procesar el comando.",
            ephemeral=True
        )

# ============ MANEJADOR DE DESCONEXIÓN ============
@bot.event
async def on_voice_state_update(member, before, after):
    """Manejar cambios de estado de voz para limpiar recursos"""
    try:
        # Si el bot fue desconectado de un canal de voz
        if member.id == bot.user.id and before.channel and not after.channel:
            guild_id = before.channel.guild.id
            await music_system.cleanup_guild(guild_id)
            logger.info(f"✅ Recursos limpiados para guild {guild_id}")
    except Exception as e:
        logger.error(f"Error en on_voice_state_update: {e}")

# ============ COMANDO DE REINICIO DE MÚSICA ============
@bot.tree.command(name="music_reset", description="Reiniciar sistema de música (para problemas)")
async def music_reset(interaction: discord.Interaction):
    """Reiniciar sistema de música en caso de problemas"""
    try:
        guild_id = interaction.guild_id
        
        # Limpiar cola actual
        if guild_id in music_system.queues:
            music_system.queues[guild_id].clear()
        
        if guild_id in music_system.current:
            music_system.current[guild_id] = None
        
        if guild_id in music_system.requests:
            music_system.requests[guild_id].clear()
        
        # Desconectar si está conectado
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
        
        await music_system.cleanup_guild(guild_id)
        
        embed = discord.Embed(
            title="🔄 Sistema de Música Reiniciado",
            description="El sistema de música ha sido reiniciado exitosamente.",
            color=0x00ff88
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        logger.error(f"Error en music_reset: {e}")
        await interaction.response.send_message(
            "❌ Error reiniciando el sistema de música",
            ephemeral=True
        )





# ============ COMANDOS DE INTERACCIÓN SOCIAL ============
@bot.tree.command(name="felizcumple", description="Envía una felicitación de cumpleaños")
@app_commands.describe(usuario="El usuario a felicitar")
async def felizcumple(interaction: discord.Interaction, usuario: discord.Member):
	"""Comando de cumpleaños mejorado"""
	embed = discord.Embed(
		title="🎉 ¡Celebraciones de Cumpleaños! 🎂",
		description=(
			f"⭐ **{usuario.display_name}** 🎈\n\n"
			f"🎂 ¡AY PAPAAA! Parece que tenemos cumpleaños hoy!\n"
			f"The players le desea un día **maravilloso**, lleno de alegrías y sorpresas 🥳🎁"
		),
		color=discord.Color.magenta()
	)
	embed.set_image(url="https://wallpapers.com/images/hd/happy-birthday-anime-wallpaper-529ageusxv02ueqp.jpg")
	embed.set_footer(text=f"De parte de {interaction.user.display_name} y todo el servidor 💖")
	
	await interaction.response.send_message(embed=embed)


@bot.tree.command(name="abrazar", description="Envía un fuerte abrazo virtual")
@app_commands.describe(usuario="El usuario a abrazar")
async def abrazar(interaction: discord.Interaction, usuario: discord.Member):
	"""Comando de abrazo optimizado con todos los links originales"""
	urls = [
		"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6KUK3rUl_EftABW5DSPZyG76hPQmB-2z1hQ&usqp=CAU",
		"https://i.pinimg.com/originals/85/dc/ef/85dcef131af84b515106955e142df54e.gif",
		"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTN4yetNRO1ky7oC6afzeO2nZp1gIj98pxSUkeSSn7m-AwaqeFzqvBFUTO2&s=10",
		"./images/17623616496654339245968767173004.gif",
		"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5b1fr9fbn_bjqCgJDNKZZI-0ptFAZ96zP2xCWK-vHxGmDmR9v5b98z_c&s=10",
		"https://i.pinimg.com/1200x/4f/3b/3b/4f3b3b7976e63222d8bda521eb5c5ab2.jpg",
		"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS33rofShkbjg4AXQrq8xgrbjP77Jc3dUKmI_X_CTsChTR6YESWeuiCKB8T&s=10",
		"https://i.imgur.com/7Bdh4C8.gif",
		"https://pm1.aminoapps.com/6452/8c2da941720ea5d7d4682b63d1ac10b74c4f0c41_hq.jpg",
		"https://i.pinimg.com/474x/34/8f/59/348f594641cb778e4dd1750cb00248bf.jpg"
	]
	
	embed = discord.Embed(
		title="✨✨ *Abrazo!* ✨✨",
		description=(
			f"⭐ **{usuario.display_name}** 🎈\n\n"
			f"Ha recibido un fuerte abrazo virtual de {interaction.user.mention}! 🤗"
		),
		color=0x00FFFF
	)
	embed.set_image(url=random.choice(urls))
	embed.set_footer(text=f"De parte de **{interaction.user.display_name}** 💖")
	
	await interaction.response.send_message(embed=embed)
	
	
# ============ SISTEMA DE COMANDOS MEJORADO ============
@bot.command(name='comandos')
async def comandos(ctx):
	"""Sistema de comandos completamente renovado"""
	embed = discord.Embed(
		title="🌸 **Yuki - Panel de Comandos** 🌸",
		description=(
			"¡Hola! Soy Yuki, tu asistente virtual. Aquí tienes todos mis comandos:\n\n"
			"**💫 COMANDOS BÁSICOS**\n"
			"`!hola` - Saludo personalizado\n"
			"`!info` - Información sobre mí\n"
			"`!200` - Estado del servidor\n"
			"`!comandos` - Este menú\n\n"
			"**INTERACCIÓN SOCIAL**\n"
			"`!besaa @usuario` - Envía un beso\n"
			"`!besame` - Versión especial\n"
			"`!qhago` - Respuesta humorística\n\n"
			"**🎵 SISTEMA DE MÚSICA**\n"
			"`/play canción` - Reproducir música\n"
			"`/pause` - Pausar/reanudar\n"
			"`/skip` - Saltar canción\n"
			"`/queue` - Ver cola\n"
			"`/leave` - Desconectar bot\n\n"
			"**🎮 OTROS COMANDOS**\n"
			"`/felizcumple @usuario` - Felicitar\n"
			"`/abrazar @usuario` - Abrazo virtual\n"
			"`/guiame` - Guía del servidor\n"
		),
		color=discord.Color.pink()
	)
	
	embed.set_footer(
		text="💖 ¡Disfruta tu tiempo en el servidor!",
		icon_url=bot.user.display_avatar.url
	)
	
	# Botón para comandos especiales
	view = View()
	
	special_button = Button(
		label="🔮 Comandos Especiales",
		style=discord.ButtonStyle.blurple,
		emoji="🌼"
	)
	
	async def special_callback(interaction: discord.Interaction):
		embed_special = discord.Embed(
			title="🔮 **Comandos Especiales**",
			description=(
				"**COMANDOS DE INTERACCIÓN**\n"
				"`/felizcumple @usuario` - Felicitación personalizada\n"
				"`/abrazar @usuario` - Abrazo virtual con GIF\n\n"
				"**📋 INFORMACIÓN DEL SERVIDOR**\n"
				"`/guiame` - Lista completa de canales\n"
				"`/evento` - Próximos eventos programados\n\n"
				"**🎮 JUEGOS Y ENTRETENIMIENTO**\n"
				"`/pixel_gift` - Juego de velocidad\n"
				"`/pixel_status` - Estado del juego\n\n"
				"*Usa estos comandos para una experiencia más interactiva!*"
			),
			color=discord.Color.purple()
		)
		await interaction.response.send_message(embed=embed_special, ephemeral=True)
	
	special_button.callback = special_callback
	view.add_item(special_button)
	
	await ctx.send(embed=embed, view=view)

# ============ SISTEMA DE EVENTOS OPTIMIZADO ============
class EventSystem:
	"""Sistema de eventos optimizado"""
	
	def __init__(self):
		self.events_file = 'eventos.json'
	
	def cargar_eventos(self) -> List[dict]:
		"""Cargar eventos desde JSON"""
		try:
			if not os.path.exists(self.events_file):
				self.crear_archivo_ejemplo()
				return []
			
			with open(self.events_file, 'r', encoding='utf-8') as f:
				data = json.load(f)
				return data if isinstance(data, list) else []
		except Exception as e:
			logger.error(f"Error cargando eventos: {e}")
			return []
	
	def crear_archivo_ejemplo(self):
		"""Crear archivo de ejemplo"""
		evento_ejemplo = [
			{
				"type": "event",
				"name": "Fiesta de Lanzamiento",
				"category": "🎉 Evento Especial",
				"details": {
					"description": "Celebración especial por el nuevo contenido",
					"date": "15 de Diciembre 2024",
					"UTC": "20:00",
					"img": "https://cdn.discordapp.com/attachments/123456789/evento1.jpg",
					"set_footer": "¡No te lo pierdas! 🎊"
				}
			}
		]
		
		with open(self.events_file, 'w', encoding='utf-8') as f:
			json.dump(evento_ejemplo, f, indent=2, ensure_ascii=False)

event_system = EventSystem()

@bot.tree.command(name="evento", description="Muestra información sobre eventos próximos")
@app_commands.describe(modo="Tipo de visualización")
@app_commands.choices(modo=[
	app_commands.Choice(name="individual", value="individual"),
	app_commands.Choice(name="lista", value="lista")
])
async def evento(interaction: discord.Interaction, modo: str = "individual"):
	"""Comando de eventos optimizado"""
	try:
		eventos = event_system.cargar_eventos()
		
		if not eventos:
			await interaction.response.send_message(
				"❌ No hay eventos programados en este momento.",
				ephemeral=True
			)
			return
		
		# Verificar canal según el modo
		if modo == "individual":
			if interaction.channel_id != CONFIG['event_channel_single']:
				await interaction.response.send_message(
					f"❌ Usa este comando en <#{CONFIG['event_channel_single']}>",
					ephemeral=True
				)
				return
			
			# Mostrar evento más próximo
			evento = eventos[0]
			embed = discord.Embed(
				title=f"🎉 {evento.get('name', 'Evento Próximo')}",
				color=0xff6b6b
			)
			
			detalles = evento.get('details', {})
			if 'description' in detalles:
				embed.description = f"**{detalles['description']}**"
			
			# Campos dinámicos
			if 'date' in detalles:
				embed.add_field(name="📅 Fecha", value=detalles['date'], inline=True)
			if 'UTC' in detalles:
				embed.add_field(name="⏰ Hora (UTC)", value=detalles['UTC'], inline=True)
			if 'category' in evento:
				embed.add_field(name="📂 Categoría", value=evento['category'], inline=True)
			
			if 'img' in detalles:
				embed.set_image(url=detalles['img'])
			
			embed.set_footer(
				text=detalles.get('set_footer', '✨ Próximo Evento • No te lo pierdas!')
			)
			
			await interaction.response.send_message(embed=embed)
			
		elif modo == "lista":
			if interaction.channel_id != CONFIG['event_channel_list']:
				await interaction.response.send_message(
					f"❌ Usa este comando en <#{CONFIG['event_channel_list']}>",
					ephemeral=True
				)
				return
			
			# Mostrar lista de eventos
			embed = discord.Embed(
				title="📅 **Calendario de Eventos**",
				description="Lista completa de eventos programados",
				color=0x2ecc71
			)
			
			for i, evento in enumerate(eventos[:10]):  # Máximo 10 eventos
				detalles = evento.get('details', {})
				valor = f"**Descripción:** {detalles.get('description', 'Sin descripción')}\n"
				
				if 'date' in detalles:
					valor += f"**Fecha:** {detalles['date']}\n"
				if 'UTC' in detalles:
					valor += f"**Hora:** {detalles['UTC']} UTC\n"
				
				embed.add_field(
					name=f"🎯 {evento.get('name', f'Evento {i+1}')}",
					value=valor,
					inline=False
				)
			
			await interaction.response.send_message(embed=embed)
			
	except Exception as e:
		logger.error(f"Error en comando evento: {e}")
		await interaction.response.send_message(
			"❌ Error al cargar los eventos",
			ephemeral=True
		)

# ============ COMANDO GUIAME ============
@bot.tree.command(
	name="guiame",
	description="Muestra lista de canales de texto disponibles"
)
async def guiame(interaction: discord.Interaction):
	if interaction.channel_id != CONFIG['guide_channel']:
		await interaction.response.send_message(
			f"❌ Este comando solo puede usarse en <#{CONFIG['guide_channel']}>",
			ephemeral=True
		)
		return
	
	canales_texto = [
		canal for canal in interaction.guild.text_channels 
		if canal.permissions_for(interaction.guild.me).read_messages
	]
	
	if not canales_texto:
		await interaction.response.send_message(
			"❌ No se encontraron canales de texto accesibles",
			ephemeral=True
		)
		return
	
	embed = discord.Embed(
		title=f"🗺️ Guía de Canales - {interaction.guild.name}",
		description="Aquí tienes todos los canales de texto disponibles:\n",
		color=discord.Color.blue()
	)
	
	for canal in canales_texto[:25]:  # Límite de campos
		descripcion = canal.topic or "Sin descripción"
		embed.add_field(
			name=f"📁 {canal.name}",
			value=f"{canal.mention}\n*{descripcion[:100]}...*",
			inline=True
		)
	
	embed.set_footer(text=f"Solicitado por {interaction.user.display_name}")
	await interaction.response.send_message(embed=embed)

# ============ SISTEMA DE ESTADÍSTICAS ============
@bot.tree.command(name="estadisticas", description="Muestra estadísticas del servidor")
async def estadisticas(interaction: discord.Interaction):
	"""Estadísticas del servidor"""
	guild = interaction.guild
	
	embed = discord.Embed(
		title=f"📊 Estadísticas de {guild.name}",
		color=discord.Color.gold()
	)
	
	# Información básica
	embed.add_field(
		name="👥 Miembros",
		value=f"Total: {guild.member_count}\n"
			  f"Humanos: {len([m for m in guild.members if not m.bot])}\n"
			  f"Bots: {len([m for m in guild.members if m.bot])}",
		inline=True
	)
	
	embed.add_field(
		name="📁 Canales",
		value=f"Texto: {len(guild.text_channels)}\n"
			  f"Voz: {len(guild.voice_channels)}\n"
			  f"Categorías: {len(guild.categories)}",
		inline=True
	)
	
	embed.add_field(
		name="🎯 Información",
		value=f"Creado: {guild.created_at.strftime('%d/%m/%Y')}\n"
			  f"Dueño: {guild.owner.mention if guild.owner else 'N/A'}\n"
			  f"Boost: Nivel {guild.premium_tier}",
		inline=True
	)
	
	# Roles (top 10)
	roles_text = ", ".join([role.mention for role in sorted(guild.roles, key=lambda r: r.position, reverse=True)[:10]])
	embed.add_field(
		name="🏷️ Roles Principales",
		value=roles_text if roles_text else "No hay roles",
		inline=False
	)
	
	embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
	embed.set_footer(text=f"Solicitado por {interaction.user.display_name}")
	
	await interaction.response.send_message(embed=embed)





# ============ CLASE DEL SISTEMA DE RECOMENDACIONES ============
class RecommendationSystem:
    def __init__(self, file_path='recomendaciones.json'):
        self.file_path = file_path
        self.recomendaciones = self._load_recommendations()
    
    def _load_recommendations(self):
        """Carga las recomendaciones desde el archivo JSON"""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Crear estructura básica si el archivo no existe
                base_structure = {
                    "juego": [],
                    "musica": [],
                    "pelicula": [],
                    "libro": [],
                    "anime": [],
                    "serie": [],
                    "podcast": []
                }
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(base_structure, file, ensure_ascii=False, indent=2)
                return base_structure
        except Exception as e:
            print(f"Error cargando recomendaciones: {e}")
            return {}
    
    def get_recommendation(self, category):
        """Obtiene una recomendación aleatoria de una categoría"""
        if category in self.recomendaciones and self.recomendaciones[category]:
            return random.choice(self.recomendaciones[category])
        return None
    
    def get_available_categories(self):
        """Obtiene las categorías disponibles"""
        return list(self.recomendaciones.keys())
    
    def add_recommendation(self, category, recommendation):
        """Añade una nueva recomendación a una categoría"""
        if category not in self.recomendaciones:
            self.recomendaciones[category] = []
        
        if recommendation not in self.recomendaciones[category]:
            self.recomendaciones[category].append(recommendation)
            self._save_recommendations()
            return True
        return False
    
    def _save_recommendations(self):
        """Guarda las recomendaciones en el archivo JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(self.recomendaciones, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando recomendaciones: {e}")

# ============ INICIALIZACIÓN DEL SISTEMA DE RECOMENDACIONES ============
recommendation_system = RecommendationSystem('recomendaciones.json')

# ============ COMANDO DE RECOMENDACIONES ============
@bot.tree.command(name="recomendacion", description="Obtén una recomendación aleatoria")
@app_commands.describe(tipo="Tipo de recomendación")
@app_commands.choices(tipo=[
    app_commands.Choice(name="🎮 Juegos", value="juego"),
    app_commands.Choice(name="🎵 Música", value="musica"),
    app_commands.Choice(name="🎬 Películas", value="pelicula"),
    app_commands.Choice(name="📚 Libros", value="libro"),
    app_commands.Choice(name="🎌 Anime", value="anime"),
    app_commands.Choice(name="📺 Series", value="serie"),
    app_commands.Choice(name="🎙️ Podcasts", value="podcast")
])
async def recomendacion(interaction: discord.Interaction, tipo: app_commands.Choice[str]):
    """Sistema de recomendaciones con choices predefinidos"""
    
    # Obtener el valor del choice seleccionado
    tipo_value = tipo.value
    
    # Obtener recomendación
    recomendacion_texto = recommendation_system.get_recommendation(tipo_value)
    
    if not recomendacion_texto:
        embed = discord.Embed(
            title="❌ Sin Recomendaciones",
            description=f"No hay recomendaciones disponibles para la categoría `{tipo_value}`.",
            color=0xe74c3c
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Emojis para cada categoría
    emojis = {
        "juego": "🎮", 
        "musica": "🎵", 
        "pelicula": "🎬", 
        "libro": "📚",
        "anime": "🎌",
        "serie": "📺",
        "podcast": "🎙️"
    }
    
    embed = discord.Embed(
        title=f"{emojis.get(tipo_value, '💫')} Recomendación de {tipo_value.title()}",
        description=recomendacion_texto,
        color=discord.Color.purple()
    )
    
    # Obtener estadísticas de la categoría
    stats = {cat: len(items) for cat, items in recommendation_system.recomendaciones.items()}
    total_en_categoria = stats.get(tipo_value, 0)
    
    embed.set_footer(
        text=f"Recomendado para {interaction.user.display_name} • {total_en_categoria} recomendaciones en esta categoría 💖"
    )
    
    await interaction.response.send_message(embed=embed)

# ============ COMANDO ALTERNATIVO CON OPCIONES DINÁMICAS ============
@bot.tree.command(name="recomendar", description="Obtén una recomendación con todas las categorías disponibles")
@app_commands.describe(tipo="Elige una categoría")
async def recomendar(interaction: discord.Interaction, tipo: str):
    """Comando alternativo que acepta cualquier categoría del JSON"""
    
    # Verificar si la categoría existe
    available_categories = recommendation_system.get_available_categories()
    if tipo not in available_categories:
        # Mostrar categorías disponibles en un embed
        embed = discord.Embed(
            title="❌ Categoría No Encontrada",
            description=(
                f"La categoría `{tipo}` no existe.\n\n"
                f"**Categorías disponibles en el sistema:**\n"
                f"{', '.join([f'`{cat}`' for cat in available_categories])}\n\n"
                f"**💡 Tip:** Usa `/recomendacion` para ver las categorías principales con menú desplegable"
            ),
            color=0xe74c3c
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Obtener recomendación
    recomendacion_texto = recommendation_system.get_recommendation(tipo)
    
    if not recomendacion_texto:
        embed = discord.Embed(
            title="❌ Sin Recomendaciones",
            description=f"No hay recomendaciones disponibles para la categoría `{tipo}`.",
            color=0xe74c3c
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    # Emojis para cada categoría
    emojis = {
        "juego": "🎮", 
        "musica": "🎵", 
        "pelicula": "🎬", 
        "libro": "📚",
        "anime": "🎌",
        "serie": "📺",
        "podcast": "🎙️"
    }
    
    embed = discord.Embed(
        title=f"{emojis.get(tipo, '💫')} Recomendación de {tipo.title()}",
        description=recomendacion_texto,
        color=discord.Color.purple()
    )
    
    # Obtener estadísticas de la categoría
    stats = {cat: len(items) for cat, items in recommendation_system.recomendaciones.items()}
    total_en_categoria = stats.get(tipo, 0)
    
    embed.set_footer(
        text=f"Recomendado para {interaction.user.display_name} • {total_en_categoria} recomendaciones en esta categoría 💖"
    )
    
    await interaction.response.send_message(embed=embed)

# ============ COMANDO PARA AÑADIR RECOMENDACIONES ============
@bot.tree.command(name="añadir_recomendacion", description="Añade una nueva recomendación al sistema")
@app_commands.describe(
    categoria="Categoría de la recomendación",
    recomendacion="La recomendación a añadir"
)
async def añadir_recomendacion(interaction: discord.Interaction, categoria: str, recomendacion: str):
    """Añade una nueva recomendación al sistema"""
    
    available_categories = recommendation_system.get_available_categories()
    
    if categoria not in available_categories:
        embed = discord.Embed(
            title="❌ Categoría Inválida",
            description=(
                f"La categoría `{categoria}` no existe.\n\n"
                f"**Categorías disponibles:**\n"
                f"{', '.join([f'`{cat}`' for cat in available_categories])}"
            ),
            color=0xe74c3c
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    if recommendation_system.add_recommendation(categoria, recomendacion):
        embed = discord.Embed(
            title="✅ Recomendación Añadida",
            description=f"Se añadió **{recomendacion}** a la categoría **{categoria}**",
            color=0x2ecc71
        )
    else:
        embed = discord.Embed(
            title="⚠️ Recomendación Duplicada",
            description=f"**{recomendacion}** ya existe en la categoría **{categoria}**",
            color=0xf39c12
        )
    
    await interaction.response.send_message(embed=embed)

# ============ COMANDO PARA VER ESTADÍSTICAS ============
@bot.tree.command(name="estadisticas_recomendaciones", description="Muestra las estadísticas del sistema de recomendaciones")
async def estadisticas_recomendaciones(interaction: discord.Interaction):
    """Muestra cuántas recomendaciones hay en cada categoría"""
    
    stats = {cat: len(items) for cat, items in recommendation_system.recomendaciones.items()}
    total_recomendaciones = sum(stats.values())
    
    embed = discord.Embed(
        title="📊 Estadísticas de Recomendaciones",
        color=discord.Color.blue()
    )
    
    for categoria, cantidad in stats.items():
        embed.add_field(
            name=f"{categoria.title()} ({cantidad})",
            value="▰" * min(cantidad, 20) + "▱" * max(0, 20 - cantidad),
            inline=False
        )
    
    embed.set_footer(text=f"Total de recomendaciones en el sistema: {total_recomendaciones}")
    
    await interaction.response.send_message(embed=embed)









# ============ COMANDO DE AYUDA MEJORADO ============
@bot.tree.command(name="recomendacion_help", description="Ayuda completa del sistema de recomendaciones")
async def recomendacion_help(interaction: discord.Interaction):
    """Mostrar ayuda completa del sistema de recomendaciones"""
    
    # Obtener categorías disponibles
    available_categories = recommendation_system.get_available_categories()
    stats = {cat: len(items) for cat, items in recommendation_system.recomendaciones.items()}
    
    embed = discord.Embed(
        title="💫 Sistema de Recomendaciones - Ayuda Completa",
        description="Descubre nuevas cosas interesantes con nuestro sistema de recomendaciones:",
        color=0xff6b6b
    )
    
    embed.add_field(
        name="🎯 Comando Principal (con Menú)",
        value=(
            "**`/recomendacion`**\n"
            "• Opciones predefinidas\n"
            "• Menú desplegable fácil de usar\n"
            "• Categorías principales garantizadas"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔧 Comando Avanzado",
        value=(
            "**`/recomendar`**\n"
            "• Acepta cualquier categoría del JSON\n"
            "• Útil para categorías personalizadas\n"
            "• Escribe el nombre exacto de la categoría"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 Comandos de Información",
        value=(
            "**`/recomendacion_list`** - Ver todas las categorías\n"
            "**`/recomendacion_stats`** - Ver estadísticas\n"
            "**`/recomendacion_add`** - Añadir recomendación (Admin)"
        ),
        inline=False
    )
    
    # Mostrar categorías disponibles
    if available_categories:
        categories_text = "\n".join([
            f"• `{cat}` ({stats.get(cat, 0)} recomendaciones)" 
            for cat in available_categories
        ])
        embed.add_field(
            name="📂 Categorías en el Sistema",
            value=categories_text,
            inline=False
        )
    
    embed.set_footer(text="¡Explora nuevas recomendaciones cada día!")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============ EVENTO ON_READY ACTUALIZADO ============
@bot.event
async def on_ready():
    """Evento on_ready con información actualizada"""
    print(f'✅ {bot.user} conectado exitosamente!')
    
    # Obtener información del owner
    try:
        app_info = await bot.application_info()
        bot.owner_id = app_info.owner.id
        print(f'👑 Owner del bot: {app_info.owner.name} ({bot.owner_id})')
    except Exception as e:
        print(f'⚠️ No se pudo obtener información del owner: {e}')
    
    # Sincronizar comandos
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} comandos sincronizados')
        
        # Mostrar lista de comandos de recomendaciones
        recomendacion_commands = [cmd for cmd in synced if 'recomendacion' in cmd.name or 'recomendar' in cmd.name]
        if recomendacion_commands:
            print('Comandos de recomendaciones disponibles:')
            for cmd in recomendacion_commands:
                print(f'   /{cmd.name} - {cmd.description}')
            
    except Exception as e:
        print(f'❌ Error sincronizando comandos: {e}')
    
    print('Sistema de recomendaciones cargado correctamente!')











# ============ SISTEMA DE VENTAS CON REGATEO CORREGIDO ============

# Configuración
OFFER_TIME = 60*5  # segundos

# Almacenamiento de ofertas activas
active_offers = {}

class BuyerOfferModal(Modal):
    def __init__(self, offer_data):
        super().__init__(title="Hacer Oferta")
        self.offer_data = offer_data
        self.price_input = TextInput(
            label="Tu Oferta",
            placeholder="Ingresa el precio que quieres pagar...",
            required=True
        )
        self.add_item(self.price_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_price = int(self.price_input.value)
            if new_price <= 0:
                await interaction.response.send_message("❌ El precio debe ser mayor a 0", ephemeral=True)
                return
            
            # Verificar que el comprador tenga suficiente dinero
            buyer_data = economy_system.get_user_data(str(self.offer_data['buyer_id']))
            if buyer_data["monedas"] < new_price:
                await interaction.response.send_message(
                    f"❌ No tienes suficientes monedas. Necesitas {new_price}🪙 pero tienes {buyer_data['monedas']}🪙",
                    ephemeral=True
                )
                return
            
            # Actualizar la oferta del comprador
            self.offer_data['buyer_offer'] = new_price
            self.offer_data['last_offer_by'] = interaction.user.id
            self.offer_data['has_pending_offer'] = True
            
            # Editar embed con nueva oferta
            embed = self.create_offer_embed()
            view = TradeView(self.offer_data)
            
            await interaction.response.edit_message(embed=embed, view=view)
            
            # Notificar en el chat
            await interaction.followup.send(
                f"💬 {interaction.user.mention} ha hecho una oferta de **{new_price}🪙** por **{self.offer_data['item_name']}**",
                ephemeral=False
            )
                
        except ValueError:
            await interaction.response.send_message("❌ Ingresa un número válido", ephemeral=True)

    def create_offer_embed(self):
        embed = discord.Embed(
            title="💰 Oferta de Venta" if self.offer_data['type'] == 'item' else "🌟 Venta de Personaje",
            color=0xf39c12,
            timestamp=discord.utils.utcnow()
        )
        
        seller = self.offer_data.get('seller')
        buyer = self.offer_data.get('buyer')
        item_name = self.offer_data.get('item_name', 'Item')
        current_price = self.offer_data.get('current_price', 0)
        buyer_offer = self.offer_data.get('buyer_offer')
        
        embed.add_field(name="👤 Vendedor", value=seller.mention, inline=True)
        embed.add_field(name="👥 Comprador", value=buyer.mention, inline=True)
        embed.add_field(
            name="🎁 Item" if self.offer_data['type'] == 'item' else "🌠 Personaje", 
            value=item_name, 
            inline=True
        )
        
        # Precio de venta actual
        embed.add_field(
            name="💰 Precio de Venta",
            value=f"**{current_price}🪙**",
            inline=True
        )
        
        # Oferta del comprador
        if buyer_offer:
            embed.add_field(
                name="💬 Tu Oferta",
                value=f"**{buyer_offer}🪙**",
                inline=True
            )
            
            # Estado de la oferta
            if buyer_offer >= current_price:
                status = "✅ Mayor o igual al precio"
                embed.add_field(name="📊 Estado", value=status, inline=True)
            else:
                difference = current_price - buyer_offer
                status = f"📉 {difference}🪙 menos"
                embed.add_field(name="📊 Estado", value=status, inline=True)
        else:
            embed.add_field(name="💬 Tu Oferta", value="❌ Sin oferta", inline=True)
            embed.add_field(name="📊 Estado", value="⏳ Esperando oferta", inline=True)
        
        # Información adicional para personajes
        if self.offer_data['type'] == 'character':
            embed.add_field(name="📺 Serie", value=self.offer_data.get('serie', 'Desconocida'), inline=True)
            embed.add_field(
                name="✨ Rareza", 
                value=f"{ANIME_RARITY_SYSTEM[self.offer_data.get('rarity', 'comun')]['emoji']} {self.offer_data.get('rarity', 'comun').title()}", 
                inline=True
            )
            embed.add_field(name="🏷️ ID", value=f"`{self.offer_data['item_id']}`", inline=True)
        else:
            embed.add_field(name="🏷️ ID", value=f"`{self.offer_data['item_id']}`", inline=True)
            embed.add_field(name=" ", value=" ", inline=True)
            embed.add_field(name=" ", value=" ", inline=True)
        
        # Información de monedas
        embed.add_field(
            name="👛 Tus Monedas",
            value=f"{economy_system.get_user_data(str(buyer.id))['monedas']}🪙",
            inline=True
        )
        
        embed.add_field(
            name="💰 Monedas del Vendedor", 
            value=f"{economy_system.get_user_data(str(seller.id))['monedas']}🪙",
            inline=True
        )
        
        # Instrucciones
        embed.add_field(
            name="💡 Cómo funciona",
            value=(
                "• **Ofertar**: Propón un precio\n"
                "• **Comprar Ahora**: Compra al precio actual\n"
                "• **El vendedor decide** si acepta tu oferta"
            ),
            inline=False
        )
        
        if self.offer_data.get('has_pending_offer'):
            embed.set_footer(text=f"⏰ Oferta pendiente • El vendedor debe aceptar • Válida por {OFFER_TIME}s")
        else:
            embed.set_footer(text=f"⏰ Esperando oferta • Válida por {OFFER_TIME}s")
        
        return embed

class SellerPriceModal(Modal):
    def __init__(self, offer_data):
        super().__init__(title="Modificar Precio de Venta")
        self.offer_data = offer_data
        self.price_input = TextInput(
            label="Nuevo Precio de Venta",
            placeholder="Ingresa el nuevo precio de venta...",
            required=True
        )
        self.add_item(self.price_input)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_price = int(self.price_input.value)
            if new_price <= 0:
                await interaction.response.send_message("❌ El precio debe ser mayor a 0", ephemeral=True)
                return
            
            # Actualizar el precio de venta
            self.offer_data['current_price'] = new_price
            self.offer_data['last_offer_by'] = interaction.user.id
            # Resetear la oferta del comprador cuando el vendedor cambia el precio
            self.offer_data['buyer_offer'] = None
            self.offer_data['has_pending_offer'] = False
            
            # Editar embed con nuevo precio
            embed = self.create_offer_embed()
            view = TradeView(self.offer_data)
            
            await interaction.response.edit_message(embed=embed, view=view)
            
            # Notificar en el chat
            await interaction.followup.send(
                f"📊 {interaction.user.mention} ha establecido el precio en **{new_price}🪙** para **{self.offer_data['item_name']}**",
                ephemeral=False
            )
                
        except ValueError:
            await interaction.response.send_message("❌ Ingresa un número válido", ephemeral=True)

    def create_offer_embed(self):
        # Reutilizar la misma función de embed
        modal = BuyerOfferModal(self.offer_data)
        return modal.create_offer_embed()

class TradeView(View):
    def __init__(self, offer_data):
        super().__init__(timeout=OFFER_TIME)
        self.offer_data = offer_data
        self.offer_id = offer_data['offer_id']
        
    async def on_timeout(self):
        if self.offer_id in active_offers:
            offer_data = active_offers[self.offer_id]
            offer_data['expired'] = True
            
            embed = discord.Embed(
                title="⏰ Oferta Expirada",
                description="El tiempo para esta oferta ha terminado",
                color=0xe74c3c
            )
            
            try:
                message = offer_data.get('message')
                if message:
                    await message.edit(embed=embed, view=None)
            except:
                pass
            
            if self.offer_id in active_offers:
                del active_offers[self.offer_id]
    
    @discord.ui.button(label="💬 Ofertar", style=discord.ButtonStyle.primary, custom_id="make_offer")
    async def make_offer(self, interaction: discord.Interaction, button: Button):
        # Solo el COMPRADOR puede hacer ofertas
        if interaction.user.id != self.offer_data['buyer_id']:
            await interaction.response.send_message("❌ Solo el comprador puede hacer ofertas", ephemeral=True)
            return
        
        modal = BuyerOfferModal(self.offer_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="✏️ Modificar Precio", style=discord.ButtonStyle.secondary, custom_id="modify_price")
    async def modify_price(self, interaction: discord.Interaction, button: Button):
        # Solo el VENDEDOR puede modificar el precio
        if interaction.user.id != self.offer_data['seller_id']:
            await interaction.response.send_message("❌ Solo el vendedor puede modificar el precio", ephemeral=True)
            return
        
        modal = SellerPriceModal(self.offer_data)
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="✅ Aceptar Oferta", style=discord.ButtonStyle.success, custom_id="accept_offer")
    async def accept_offer(self, interaction: discord.Interaction, button: Button):
        # CORREGIDO: Solo el VENDEDOR puede aceptar ofertas
        if interaction.user.id != self.offer_data['seller_id']:
            await interaction.response.send_message("❌ Solo el vendedor puede aceptar ofertas", ephemeral=True)
            return
        
        # Verificar que hay una oferta pendiente del comprador
        if not self.offer_data.get('has_pending_offer') or not self.offer_data.get('buyer_offer'):
            await interaction.response.send_message("❌ No hay una oferta pendiente del comprador para aceptar", ephemeral=True)
            return
        
        # CORREGIDO: Usar la oferta del comprador cuando el vendedor acepta
        try:
            item_id = self.offer_data['item_id']
            seller_id = str(self.offer_data['seller_id'])
            buyer_id = str(self.offer_data['buyer_id'])
            price = self.offer_data['buyer_offer']  # CORRECCIÓN: Usar la oferta del comprador
            
            # Verificar que el comprador tiene suficiente dinero
            buyer_data = economy_system.get_user_data(buyer_id)
            if buyer_data["monedas"] < price:
                await interaction.response.send_message(
                    f"❌ El comprador no tiene suficientes monedas. Necesita {price}🪙 pero tiene {buyer_data['monedas']}🪙",
                    ephemeral=True
                )
                return
            
            # Verificar que el vendedor aún tiene el item
            if self.offer_data['type'] == 'character':
                character = anime_gacha_system.get_character_by_id(seller_id, item_id)
                if not character:
                    await interaction.response.send_message("❌ El personaje ya no está disponible", ephemeral=True)
                    return
                
                # Verificar espacio del comprador
                buyer_gacha_data = anime_gacha_system.get_user_data(buyer_id)
                if len(buyer_gacha_data.get("personajes", [])) >= GACHA_CONFIG['max_inventory_size']:
                    await interaction.response.send_message("❌ La colección del comprador está llena", ephemeral=True)
                    return
                
                # Realizar transferencia del personaje
                success, message = await anime_gacha_system.transferir_personaje(seller_id, buyer_id, item_id)
                
            else:  # item
                user_data = economy_system.get_user_data(seller_id)
                item_found = any(item.get('unique_id') == item_id or item.get('id') == item_id for item in user_data.get("inventario", []))
                if not item_found:
                    await interaction.response.send_message("❌ El item ya no está disponible", ephemeral=True)
                    return
                
                # Verificar espacio del comprador
                buyer_economy_data = economy_system.get_user_data(buyer_id)
                if len(buyer_economy_data.get("inventario", [])) >= ECONOMY_CONFIG['max_inventory_size']:
                    await interaction.response.send_message("❌ El inventario del comprador está lleno", ephemeral=True)
                    return
                
                # Realizar transferencia del item
                success, message = await economy_system.transfer_item(seller_id, buyer_id, item_id)
            
            if success:
                # Transferir monedas al PRECIO DE LA OFERTA DEL COMPRADOR
                await economy_system.remove_coins(buyer_id, price)
                await economy_system.add_coins(seller_id, price)
                
                # Crear embed de éxito
                if self.offer_data['type'] == 'character':
                    embed = self.create_character_success_embed(price, buyer_data, economy_system.get_user_data(seller_id))
                else:
                    embed = self.create_item_success_embed(price, buyer_data, economy_system.get_user_data(seller_id))
                
            else:
                embed = discord.Embed(
                    title="❌ Error en Transacción",
                    description=f"No se pudo transferir el item: {message}",
                    color=0xe74c3c
                )
                
        except Exception as e:
            print(f"Error en transacción de venta: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error al procesar la venta: {str(e)}",
                color=0xe74c3c
            )
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Limpiar oferta
        if self.offer_id in active_offers:
            del active_offers[self.offer_id]
    
    @discord.ui.button(label="🛒 Comprar Ahora", style=discord.ButtonStyle.success, custom_id="buy_now")
    async def buy_now(self, interaction: discord.Interaction, button: Button):
        # El COMPRADOR puede comprar inmediatamente al precio actual
        if interaction.user.id != self.offer_data['buyer_id']:
            await interaction.response.send_message("❌ Solo el comprador puede comprar el item", ephemeral=True)
            return
        
        # CORRECTO: Usar el precio actual (del vendedor) para compra inmediata
        try:
            item_id = self.offer_data['item_id']
            seller_id = str(self.offer_data['seller_id'])
            buyer_id = str(self.offer_data['buyer_id'])
            price = self.offer_data['current_price']  # Precio establecido por el vendedor
            
            # Verificar que el comprador tiene suficiente dinero
            buyer_data = economy_system.get_user_data(buyer_id)
            if buyer_data["monedas"] < price:
                await interaction.response.send_message(
                    f"❌ No tienes suficientes monedas. Necesitas {price}🪙 pero tienes {buyer_data['monedas']}🪙",
                    ephemeral=True
                )
                return
            
            # Verificar que el vendedor aún tiene el item
            if self.offer_data['type'] == 'character':
                character = anime_gacha_system.get_character_by_id(seller_id, item_id)
                if not character:
                    await interaction.response.send_message("❌ El personaje ya no está disponible", ephemeral=True)
                    return
                
                # Verificar espacio del comprador
                buyer_gacha_data = anime_gacha_system.get_user_data(buyer_id)
                if len(buyer_gacha_data.get("personajes", [])) >= GACHA_CONFIG['max_inventory_size']:
                    await interaction.response.send_message("❌ Tu colección de personajes está llena", ephemeral=True)
                    return
                
                # Realizar transferencia del personaje
                success, message = await anime_gacha_system.transferir_personaje(seller_id, buyer_id, item_id)
                
            else:  # item
                user_data = economy_system.get_user_data(seller_id)
                item_found = any(item.get('unique_id') == item_id or item.get('id') == item_id for item in user_data.get("inventario", []))
                if not item_found:
                    await interaction.response.send_message("❌ El item ya no está disponible", ephemeral=True)
                    return
                
                # Verificar espacio del comprador
                buyer_economy_data = economy_system.get_user_data(buyer_id)
                if len(buyer_economy_data.get("inventario", [])) >= ECONOMY_CONFIG['max_inventory_size']:
                    await interaction.response.send_message("❌ Tu inventario está lleno", ephemeral=True)
                    return
                
                # Realizar transferencia del item
                success, message = await economy_system.transfer_item(seller_id, buyer_id, item_id)
            
            if success:
                # Transferir monedas al PRECIO DE VENTA
                await economy_system.remove_coins(buyer_id, price)
                await economy_system.add_coins(seller_id, price)
                
                # Crear embed de éxito
                if self.offer_data['type'] == 'character':
                    embed = self.create_character_success_embed(price, buyer_data, economy_system.get_user_data(seller_id))
                else:
                    embed = self.create_item_success_embed(price, buyer_data, economy_system.get_user_data(seller_id))
                
            else:
                embed = discord.Embed(
                    title="❌ Error en Transacción",
                    description=f"No se pudo transferir el item: {message}",
                    color=0xe74c3c
                )
                
        except Exception as e:
            print(f"Error en transacción de compra: {e}")
            embed = discord.Embed(
                title="❌ Error",
                description=f"Error al procesar la compra: {str(e)}",
                color=0xe74c3c
            )
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Limpiar oferta
        if self.offer_id in active_offers:
            del active_offers[self.offer_id]
    
    def create_item_success_embed(self, price, buyer_data, seller_data):
        embed = discord.Embed(
            title="✅ Venta Completada",
            description=f"¡{self.offer_data['seller'].mention} ha **aceptado la oferta** y vendido **{self.offer_data['item_name']}** a {self.offer_data['buyer'].mention} por **{price}🪙**!",
            color=0x2ecc71
        )
        
        embed.add_field(
            name="💰 Transacción Aceptada",
            value=(
                f"**Oferta del comprador:** {price}🪙\n"
                f"**Vendedor ({self.offer_data['seller'].mention}):** +{price}🪙 (Total: {seller_data['monedas']}🪙)\n"
                f"**Comprador ({self.offer_data['buyer'].mention}):** -{price}🪙 (Total: {buyer_data['monedas']}🪙)"
            ),
            inline=False
        )
        
        return embed
    
    def create_character_success_embed(self, price, buyer_data, seller_data):
        embed = discord.Embed(
            title="🌟 ¡Oferta Aceptada!",
            description=f"¡{self.offer_data['seller'].mention} ha **aceptado la oferta** y vendido a **{self.offer_data['item_name']}** a {self.offer_data['buyer'].mention} por **{price}🪙**!",
            color=0x9b59b6
        )
        
        if self.offer_data.get('image_url'):
            embed.set_thumbnail(url=self.offer_data['image_url'])
        
        embed.add_field(
            name="💰 Transacción Aceptada",
            value=(
                f"**Oferta del comprador:** {price}🪙\n"
                f"**Vendedor ({self.offer_data['seller'].mention}):** +{price}🪙 (Total: {seller_data['monedas']}🪙)\n"
                f"**Comprador ({self.offer_data['buyer'].mention}):** -{price}🪙 (Total: {buyer_data['monedas']}🪙)"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🌠 Personaje Transferido",
            value=(
                f"**{self.offer_data['item_name']}**\n"
                f"**Serie:** {self.offer_data.get('serie', 'Desconocida')}\n"
                f"**Rareza:** {self.offer_data.get('rarity', 'comun').title()}"
            ),
            inline=False
        )
        
        return embed
    
    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.danger, custom_id="cancel_offer")
    async def cancel_offer(self, interaction: discord.Interaction, button: Button):
        # Tanto vendedor como comprador pueden cancelar
        if interaction.user.id not in [self.offer_data['seller_id'], self.offer_data['buyer_id']]:
            await interaction.response.send_message("❌ Solo el vendedor o comprador pueden cancelar esta oferta", ephemeral=True)
            return
        
        role = "vendedor" if interaction.user.id == self.offer_data['seller_id'] else "comprador"
        
        embed = discord.Embed(
            title="❌ Oferta Cancelada",
            description=f"El {role} ha cancelado esta oferta",
            color=0xe74c3c
        )
        
        await interaction.response.edit_message(embed=embed, view=None)
        
        # Limpiar oferta
        if self.offer_id in active_offers:
            del active_offers[self.offer_id]
            
            












            
            
            
            
            
            
            
            
            



















#

# ============ SISTEMA DE ECONOMÍA Y GACHA ============

#

@bot.command(name='pagar')
async def pay(ctx, mencion: discord.Member, cantidad: int):
    """Transferir monedas a otro usuario"""
    try:
        # Validaciones básicas
        if mencion.id == ctx.author.id:
            await ctx.send("❌ No puedes transferir monedas a ti mismo.\nNo van a multiplicarse.")
            return
        if cantidad < 0:
        	await ctx.send(">>> (i) Para realizar cobros usa `!cobrar`")
        	return
        if cantidad == 0:
            await ctx.send("La cantidad debe ser al menos 1🪙 moneda")
            return
        
        # Obtener datos de ambos usuarios
        user_from_data = economy_system.get_user_data(str(ctx.author.id))
        user_to_data = economy_system.get_user_data(str(mencion.id))
        
        # Verificar si el remitente tiene suficientes monedas
        if user_from_data["monedas"] < cantidad:
            await ctx.send(f"❌ No tienes suficientes monedas. Tienes {user_from_data['monedas']} monedas")
            return
        
        # Realizar la transferencia
        user_from_data["monedas"] -= cantidad
        user_to_data["monedas"] += cantidad
        
        # Guardar los cambios
        await economy_system._async_save()
        
        # Crear embed de confirmación
        embed = discord.Embed(
            title="✅ Transferencia Exitosa",
            description=f"Has transferido **{cantidad}** moneda(s) a {mencion.mention}",
            color=0x00ff88
        )
        
        # Añadir información de saldos actualizados
        embed.add_field(
            name="💰 Saldos actualizados",
            value=(
                f"**{ctx.author.mention}:** {user_from_data['monedas']} monedas (-{cantidad})\n"
                f"**{mencion.mention}:** {user_to_data['monedas']} monedas (+{cantidad})"
            ),
            inline=False
        )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        print(f"Error en comando pay: {e}")
        await ctx.send("❌ Error al realizar la transferencia")







ECONOMY_CONFIG = {
    'daily_coins': 150,
    'gacha_cost': 50,
    'starting_coins': 500,
    'max_inventory_size': 2**8
}

# Sistema de rarezas y probabilidades
RARITY_SYSTEM = {
    "comun": {"prob": 60, "color": 0x808080, "multiplier": 1.0},
    "raro": {"prob": 25, "color": 0x0070DD, "multiplier": 2.5},
    "epico": {"prob": 10, "color": 0xA335EE, "multiplier": 5.0},
    "legendario": {"prob": 4, "color": 0xFF8000, "multiplier": 12.5},
    "mitico": {"prob": 1, "color": 0xE6CC80, "multiplier": 25.0}
}

# Base de datos de items disponibles
def cargar_items_desde_json():
    """Cargar items directamente desde el archivo JSON"""
    try:
        with open('gacha_items.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("gacha_items.json no encontrado.")
      
    except Exception as e:
        print(f"❌ Error cargando artículos: {e}")
        return {}

GACHA_ITEMS = cargar_items_desde_json()


class EconomySystem:
    """Sistema de economía optimizado para alto tráfico"""
    
    def __init__(self):
        self.data_file = 'economy_data.json'
        self._cache = {}
        self._lock = asyncio.Lock()
        self._load_data()
    
    def _load_data(self):
        """Cargar datos desde JSON"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
            else:
                self._cache = {"users": {}, "last_daily": {}}
                self._save_data()
        except Exception as e:
            print(f"❌ Error cargando datos económicos: {e}")
            self._cache = {"users": {}, "last_daily": {}}
    
    def _save_data(self):
        """Guardar datos a JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando datos económicos: {e}")
    
    async def _atomic_operation(self, operation):
        """Ejecutar operación atómicamente con lock"""
        async with self._lock:
            try:
                result = await operation()
                asyncio.create_task(self._async_save())
                return result
            except Exception as e:
                print(f"❌ Error en operación atómica: {e}")
                raise
    
    async def _async_save(self):
        """Guardar de forma asíncrona"""
        await asyncio.get_event_loop().run_in_executor(None, self._save_data)
    
    def get_user_data(self, user_id: str):
        """Obtener datos de usuario de forma segura"""
        user_id_str = str(user_id)
        if user_id_str not in self._cache["users"]:
            self._cache["users"][user_id_str] = {
                "monedas": ECONOMY_CONFIG['starting_coins'],
                "inventario": [],
                "personajes_obtenidos": [],
                "total_gachas": 0
            }
        return self._cache["users"][user_id_str]
    
    async def add_coins(self, user_id: str, amount: int):
        """Añadir monedas a usuario"""
        async def operation():
            user_data = self.get_user_data(user_id)
            user_data["monedas"] += amount
            return user_data["monedas"]
        
        return await self._atomic_operation(operation)
    
    async def remove_coins(self, user_id: str, amount: int):
        """Remover monedas de usuario"""
        async def operation():
            user_data = self.get_user_data(user_id)
            if user_data["monedas"] < amount:
                return False
            user_data["monedas"] -= amount
            return True
        
        return await self._atomic_operation(operation)
    
    def get_rarity(self):
        """Obtener rareza basada en probabilidades"""
        rand = random.random() * 100
        cumulative = 0
        
        for rarity, data in RARITY_SYSTEM.items():
            cumulative += data["prob"]
            if rand <= cumulative:
                return rarity
        
        return "comun"
    
    def get_random_item(self, rarity: str):
        """Obtener item aleatorio de una rareza específica"""
        available_items = []
        for category in GACHA_ITEMS.values():
            for item in category:
                if item["rareza"] == rarity:
                    available_items.append(item)
        
        if available_items:
            item = random.choice(available_items).copy()
            item["unique_id"] = str(uuid.uuid4())[:8]
            item["obtenido_en"] = datetime.now().isoformat()
            return item
        else:
            return {
                "id": "fallback",
                "unique_id": str(uuid.uuid4())[:8],
                "nombre": f"Item {rarity.capitalize()}",
                "tipo": "especial",
                "rareza": rarity,
                "valor": RARITY_SYSTEM[rarity]["multiplier"] * 20,
                "obtenido_en": datetime.now().isoformat()
            }
    
    async def gacha_pull(self, user_id: str):
        """Realizar un pull del gacha"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            if user_data["monedas"] < ECONOMY_CONFIG['gacha_cost']:
                return None, "❌ No tienes suficientes monedas"
            
            if len(user_data["inventario"]) >= ECONOMY_CONFIG['max_inventory_size']:
                return None, "❌ Tu inventario está lleno"
            
            rarity = self.get_rarity()
            item = self.get_random_item(rarity)
            
            user_data["inventario"].append(item)
            user_data["monedas"] -= ECONOMY_CONFIG['gacha_cost']
            user_data["total_gachas"] += 1
            
            if item["tipo"] == "personaje":
                user_data["personajes_obtenidos"].append(item["id"])
            
            return item, f"🎉 ¡Has obtenido un item {rarity.upper()}!"
        
        return await self._atomic_operation(operation)
    
    async def get_inventory(self, user_id: str, page: int = 1):
        """Obtener inventario paginado"""
        user_data = self.get_user_data(user_id)
        inventory = user_data["inventario"]
        
        items_per_page = 10
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        paginated_items = inventory[start_idx:end_idx]
        total_pages = max(1, (len(inventory) + items_per_page - 1) // items_per_page)
        
        return paginated_items, total_pages, len(inventory)
    
    async def transfer_item(self, from_user_id: str, to_user_id: str, item_unique_id: str):
        """Transferir item entre usuarios"""
        async def operation():
            from_user = self.get_user_data(from_user_id)
            to_user = self.get_user_data(to_user_id)
            
            item_index = None
            item_to_transfer = None
            
            for i, item in enumerate(from_user["inventario"]):
                if item.get("unique_id") == item_unique_id:
                    item_index = i
                    item_to_transfer = item
                    break
            
            if item_index is None:
                return False, "❌ Item no encontrado en tu inventario"
            
            if len(to_user["inventario"]) >= ECONOMY_CONFIG['max_inventory_size']:
                return False, "❌ El inventario del destinatario está lleno"
            
            from_user["inventario"].pop(item_index)
            to_user["inventario"].append(item_to_transfer)
            
            return True, "✅ Item transferido exitosamente"
        
        return await self._atomic_operation(operation)
    
    async def sell_item(self, user_id: str, item_unique_id: str):
        """Vender item por monedas"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            item_index = None
            item_to_sell = None
            
            for i, item in enumerate(user_data["inventario"]):
                if item.get("unique_id") == item_unique_id:
                    item_index = i
                    item_to_sell = item
                    break
            
            if item_index is None:
                return False, "❌ Item no encontrado en tu inventario"
            
            sell_value = int(item_to_sell["valor"] * 0.7)
            
            user_data["inventario"].pop(item_index)
            user_data["monedas"] += sell_value
            
            return True, f"✅ Item vendido por {sell_value} monedas"
        
        return await self._atomic_operation(operation)
    
    async def claim_daily(self, user_id: str):
        """Reclamar recompensa diaria"""
        async def operation():
            user_id_str = str(user_id)
            today = datetime.now().date().isoformat()
            
            if user_id_str in self._cache["last_daily"]:
                last_claim = self._cache["last_daily"][user_id_str]
                if last_claim == today:
                    return False, "❌ Ya reclamaste tu recompensa diaria hoy"
            
            user_data = self.get_user_data(user_id)
            user_data["monedas"] += ECONOMY_CONFIG['daily_coins']
            self._cache["last_daily"][user_id_str] = today
            
            return True, f"✅ Recompensa diaria de {ECONOMY_CONFIG['daily_coins']} monedas obtenida"
        
        return await self._atomic_operation(operation)

# Instancia global del sistema económico
economy_system = EconomySystem()

# ============ SISTEMA DE GACHA DE PERSONAJES ============
# ============ SISTEMA DE GACHA DE PERSONAJES ============
GACHA_CONFIG = {
    'amuleto_cost': 750,
    'coins_per_week': 127,
    'claim_cooldown_days': 7,
    'starting_amuleto': 15,
    'max_inventory_size': 2**10
}

ANIME_RARITY_SYSTEM = {
    "comun": {"prob": 55, "color": 0x808080, "coin_multiplier": 1.0, "emoji": "🌱"},
    "raro": {"prob": 30, "color": 0x0070DD, "coin_multiplier": 1.5, "emoji": "💠"},
    "epico": {"prob": 10, "color": 0xA335EE, "coin_multiplier": 2.0, "emoji": "👑"},
    "legendario": {"prob": 4, "color": 0xFF8000, "coin_multiplier": 3.0, "emoji": "🌼"},
    "mitico": {"prob": 1, "color": 0xE6CC80, "coin_multiplier": 8.0, "emoji": "🌠"}
}

# CARGAR DIRECTAMENTE DESDE JSON
def cargar_personajes_desde_json():
    """Cargar personajes directamente desde el archivo JSON"""
    try:
        with open('personajes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            personajes = data.get('personajes', [])
            print(f"✅ Cargados {len(personajes)} personajes desde personajes.json")
            return personajes
    except FileNotFoundError:
        print("❌ personajes.json no encontrado. Creando archivo de ejemplo...")
        # Crear archivo de ejemplo
        datos_ejemplo = {
            "personajes": [
                {
                    "id": "ejemplo_001",
                    "nombre": "Naruto Uzumaki",
                    "serie": "Naruto", 
                    "rareza": "comun",
                    "image_url": "https://example.com/naruto.jpg",
                    "descripcion": "Ejemplo - modificar personajes.json"
                }
            ]
        }
        with open('personajes.json', 'w', encoding='utf-8') as f:
            json.dump(datos_ejemplo, f, indent=2, ensure_ascii=False)
        return datos_ejemplo['personajes']
    except Exception as e:
        print(f"❌ Error cargando personajes: {e}")
        return []

ANIME_CHARACTERS = cargar_personajes_desde_json()


def recargar_personajes():
    """Recargar personajes (útil si modificas el JSON con el bot encendido)"""
    global ANIME_CHARACTERS
    ANIME_CHARACTERS = cargar_personajes_desde_json()
    return len(ANIME_CHARACTERS)
    
def recargar_items():
	global GACHA_ITEMS
	GACHA_ITEMS = cargar_items_desde_json()
	return len(GACHA_ITEMS)
	
@bot.command(name='recargar_p')
async def recargar_p(ctx):
    """Recargar personajes desde JSON"""
    try:
        cantidad = recargar_personajes()
        cantidad_items = recargar_items()
        await ctx.send(f" Recargados {cantidad} personajes y {cantidad_items} Categorías de articulos de ≈50c/u")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        
        
class AnimeGachaSystem:
    """Sistema de gacha para personajes de anime - CORREGIDO"""
    
    def __init__(self):
        self.data_file = 'anime_gacha_data.json'
        self._cache = {}
        self._lock = asyncio.Lock()
        self._load_data()
    
    def _load_data(self):
        """Cargar datos desde JSON - CORREGIDO"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
                    # Convertir lists de vuelta a sets
                    for user_id, user_data in self._cache.get("users", {}).items():
                        if "personajes_unicos" in user_data and isinstance(user_data["personajes_unicos"], list):
                            user_data["personajes_unicos"] = set(user_data["personajes_unicos"])
            else:
                self._cache = {
                    "users": {},
                    "global_stats": {
                        "total_invocaciones": 0,
                        "personajes_obtenidos": {},
                        "ultimo_mitico": None
                    },
                    "mercado": []
                }
                self._save_data()
        except Exception as e:
            print(f"❌ Error cargando datos gacha: {e}")
            self._cache = {
                "users": {}, 
                "global_stats": {"total_invocaciones": 0, "personajes_obtenidos": {}, "ultimo_mitico": None}, 
                "mercado": []
            }
    
    def _save_data(self):
        try:
            # Crear copia para serialización segura
            cache_to_save = json.loads(json.dumps(self._cache, default=self._json_serializer))
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(cache_to_save, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando datos gacha: {e}")
    
    def _json_serializer(self, obj):
        """Serializador personalizado para tipos no serializables"""
        if isinstance(obj, set):
            return list(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    async def _atomic_operation(self, operation):
        """Ejecutar operación atómicamente con lock"""
        async with self._lock:
            try:
                result = await operation()
                asyncio.create_task(self._async_save())
                return result
            except Exception as e:
                print(f"❌ Error en operación atómica gacha: {e}")
                raise
    
    async def _async_save(self):
        """Guardar de forma asíncrona"""
        await asyncio.get_event_loop().run_in_executor(None, self._save_data)
    
    def get_user_data(self, user_id: str):
        """Obtener datos de usuario de forma segura - CORREGIDO"""
        user_id_str = str(user_id)
        if user_id_str not in self._cache["users"]:
            self._cache["users"][user_id_str] = {
                "amuleto": GACHA_CONFIG['starting_amuleto'],
                "personajes": [],
                "ultimo_claim": None,
                "total_invocaciones": 0,
                "personajes_unicos": set(),  # Set internamente
                "historial_invocaciones": []
            }
        return self._cache["users"][user_id_str]
    
    def get_rarity(self):
        """Obtener rareza basada en probabilidades"""
        rand = random.random() * 100
        cumulative = 0
        
        for rarity, data in ANIME_RARITY_SYSTEM.items():
            cumulative += data["prob"]
            if rand <= cumulative:
                return rarity
        
        return "comun"
    
    def get_random_character(self, rarity: str):
        """Obtener personaje aleatorio de una rareza específica"""
        available_chars = [char for char in ANIME_CHARACTERS if char["rareza"] == rarity]
        
        if available_chars:
            char = random.choice(available_chars).copy()
            char["unique_id"] = str(uuid.uuid4())[:8]
            char["obtenido_en"] = datetime.now().isoformat()
            char["ultimo_claim"] = None
            return char
        else:
            return {
                "id": f"fallback_{rarity}",
                "unique_id": str(uuid.uuid4())[:8],
                "nombre": f"Personaje {rarity.capitalize()}",
                "serie": "Sistema",
                "rareza": rarity,
                "image_url": None,
                "descripcion": f"Un personaje misterioso de rareza {rarity}",
                "obtenido_en": datetime.now().isoformat(),
                "ultimo_claim": None
            }
    
    async def invocar_personaje(self, user_id: str, use_amuleto: bool = True):
        """Realizar una invocación de personaje"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            if use_amuleto:
                if user_data["amuleto"] < 1:
                    return None, "❌ No tienes amuletos de invocación"
                user_data["amuleto"] -= 1
            else:
                user_economy_data = economy_system.get_user_data(user_id)
                if user_economy_data["monedas"] < GACHA_CONFIG['amuleto_cost']:
                    return None, f"❌ No tienes suficientes monedas. Necesitas {GACHA_CONFIG['amuleto_cost']}"
                user_economy_data["monedas"] -= GACHA_CONFIG['amuleto_cost']
            
            if len(user_data["personajes"]) >= GACHA_CONFIG['max_inventory_size']:
                return None, "❌ Tu inventario de personajes está lleno"
            
            rarity = self.get_rarity()
            character = self.get_random_character(rarity)
            
            user_data["personajes"].append(character)
            user_data["total_invocaciones"] += 1
            user_data["personajes_unicos"].add(character["id"])
            user_data["historial_invocaciones"].append({
                "character_id": character["id"],
                "timestamp": datetime.now().isoformat(),
                "rareza": rarity
            })
            
            user_data["historial_invocaciones"] = user_data["historial_invocaciones"][-50:]
            
            self._cache["global_stats"]["total_invocaciones"] += 1
            self._cache["global_stats"]["personajes_obtenidos"][character["id"]] = \
                self._cache["global_stats"]["personajes_obtenidos"].get(character["id"], 0) + 1
            
            if rarity == "mitico":
                self._cache["global_stats"]["ultimo_mitico"] = {
                    "user_id": user_id,
                    "character": character["nombre"],
                    "timestamp": datetime.now().isoformat()
                }
            
            return character, f"🎉 ¡Has invocado a {character['nombre']}!"
        
        return await self._atomic_operation(operation)
    
    async def claim_coins(self, user_id: str):
        """Reclamar monedas de los personajes - CORREGIDO"""
        async def operation():
            user_data = self.get_user_data(user_id)
            now = datetime.now()
            
            if user_data["ultimo_claim"]:
                last_claim = datetime.fromisoformat(user_data["ultimo_claim"])
                if now - last_claim < timedelta(hours=23):  # CORREGIDO: timedelta importado
                    next_claim = last_claim + timedelta(hours=24)
                    time_left = next_claim - now
                    hours = int(time_left.seconds / 3600)
                    minutes = int((time_left.seconds % 3600) / 60)
                    return None, f"⏰ Ya reclamaste hoy. Podrás reclamar nuevamente en {hours}h {minutes}m"
            
            total_coins = 0
            characters_claimed = 0
            
            for character in user_data["personajes"]:
                if not character["ultimo_claim"]:
                    can_claim = True
                else:
                    last_claim = datetime.fromisoformat(character["ultimo_claim"])
                    can_claim = (now - last_claim) >= timedelta(days=GACHA_CONFIG['claim_cooldown_days'])
                
                if can_claim:
                    rarity_multiplier = ANIME_RARITY_SYSTEM[character["rareza"]]["coin_multiplier"]
                    coins_earned = int(GACHA_CONFIG['coins_per_week'] * rarity_multiplier)
                    total_coins += coins_earned
                    characters_claimed += 1
                    character["ultimo_claim"] = now.isoformat()
            
            if total_coins > 0:
                user_data["ultimo_claim"] = now.isoformat()
                await economy_system.add_coins(user_id, total_coins)
                return total_coins, characters_claimed
            else:
                return None, "❌ No hay personajes listos para reclamar monedas"
        
        return await self._atomic_operation(operation)
    
    async def add_amuleto(self, user_id: str, amount: int = 1):
        """Añadir amuletos a un usuario"""
        async def operation():
            user_data = self.get_user_data(user_id)
            user_data["amuleto"] += amount
            return user_data["amuleto"]
        
        return await self._atomic_operation(operation)
    
    async def get_user_stats(self, user_id: str):
        """Obtener estadísticas del usuario"""
        user_data = self.get_user_data(user_id)
        
        rarity_dist = {}
        for character in user_data["personajes"]:
            rareza = character["rareza"]
            rarity_dist[rareza] = rarity_dist.get(rareza, 0) + 1
        
        ready_for_claim = 0
        now = datetime.now()
        
        for character in user_data["personajes"]:
            if not character["ultimo_claim"]:
                ready_for_claim += 1
            else:
                last_claim = datetime.fromisoformat(character["ultimo_claim"])
                if (now - last_claim) >= timedelta(days=GACHA_CONFIG['claim_cooldown_days']):
                    ready_for_claim += 1
        
        return {
            "total_personajes": len(user_data["personajes"]),
            "personajes_unicos": len(user_data["personajes_unicos"]),
            "total_invocaciones": user_data["total_invocaciones"],
            "amuleto": user_data["amuleto"],
            "rarity_dist": rarity_dist,
            "ready_for_claim": ready_for_claim,
            "ultimo_claim": user_data["ultimo_claim"]
        }

    def get_character_by_id(self, user_id: str, character_unique_id: str):
        """Obtener un personaje específico por su ID único"""
        user_data = self.get_user_data(user_id)
        for character in user_data["personajes"]:
            if character.get("unique_id") == character_unique_id:
                return character
        return None

    async def transferir_personaje(self, from_user_id: str, to_user_id: str, character_unique_id: str):
        """Transferir personaje entre usuarios"""
        async def operation():
            from_user = self.get_user_data(from_user_id)
            to_user = self.get_user_data(to_user_id)
            
            character_index = None
            character_to_transfer = None
            
            for i, character in enumerate(from_user["personajes"]):
                if character.get("unique_id") == character_unique_id:
                    character_index = i
                    character_to_transfer = character
                    break
            
            if character_index is None:
                return False, "❌ Personaje no encontrado en tu colección"
            
            if len(to_user["personajes"]) >= GACHA_CONFIG['max_inventory_size']:
                return False, "❌ La colección del destinatario está llena"
            
            from_user["personajes"].pop(character_index)
            to_user["personajes"].append(character_to_transfer)
            
            return True, "✅ Personaje transferido exitosamente"
        
        return await self._atomic_operation(operation)

    async def vender_publico(self, user_id: str, character_unique_id: str, precio: int):
        """Poner personaje en venta pública"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            character_index = None
            character_to_sell = None
            
            for i, character in enumerate(user_data["personajes"]):
                if character.get("unique_id") == character_unique_id:
                    character_index = i
                    character_to_sell = character
                    break
            
            if character_index is None:
                return False, "❌ Personaje no encontrado en tu colección"
            
            if precio < 1:
                return False, "❌ El precio debe ser al menos 1 moneda"
            
            venta_id = str(uuid.uuid4())[:8]
            venta = {
                "venta_id": venta_id,
                "vendedor_id": user_id,
                "character": character_to_sell,
                "precio": precio,
                "fecha_publicacion": datetime.now().isoformat()
            }
            
            user_data["personajes"].pop(character_index)
            self._cache["mercado"].append(venta)
            
            return True, venta_id
        
        return await self._atomic_operation(operation)

    async def comprar_publico(self, user_id: str, venta_id: str):
        """Comprar personaje del mercado público"""
        async def operation():
            user_data = self.get_user_data(user_id)
            mercado = self._cache["mercado"]
            
            venta_index = None
            venta_seleccionada = None
            
            for i, venta in enumerate(mercado):
                if venta["venta_id"] == venta_id:
                    venta_index = i
                    venta_seleccionada = venta
                    break
            
            if venta_index is None:
                return False, "❌ Venta no encontrada en el mercado"
            
            if venta_seleccionada["vendedor_id"] == user_id:
                return False, "❌ No puedes comprar tu propio personaje"
            
            if len(user_data["personajes"]) >= GACHA_CONFIG['max_inventory_size']:
                return False, "❌ Tu inventario de personajes está lleno"
            
            user_economy_data = economy_system.get_user_data(user_id)
            if user_economy_data["monedas"] < venta_seleccionada["precio"]:
                return False, f"❌ No tienes suficientes monedas. Necesitas {venta_seleccionada['precio']}"
            
            user_economy_data["monedas"] -= venta_seleccionada["precio"]
            vendedor_economy_data = economy_system.get_user_data(venta_seleccionada["vendedor_id"])
            vendedor_economy_data["monedas"] += venta_seleccionada["precio"]
            
            user_data["personajes"].append(venta_seleccionada["character"])
            mercado.pop(venta_index)
            
            return True, venta_seleccionada["character"]
        
        return await self._atomic_operation(operation)

    def get_mercado(self, page: int = 1):
        """Obtener items del mercado paginados"""
        mercado = self._cache["mercado"]
        
        items_per_page = 5
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        paginated_items = mercado[start_idx:end_idx]
        total_pages = max(1, (len(mercado) + items_per_page - 1) // items_per_page)
        
        return paginated_items, total_pages, len(mercado)

# Instancia global del sistema gacha
anime_gacha_system = AnimeGachaSystem()

# ============ COMANDOS ============

@bot.command(name='gacha')
async def gacha(ctx):
    """Usar el sistema gacha"""
    try:
        embed = discord.Embed(
            title="🎰 Sistema Gacha",
            description=(
                f"**Costo:** {ECONOMY_CONFIG['gacha_cost']} monedas\n\n"
                "**Probabilidades:**\n"
                "• Común: 60%\n• Raro: 25%\n• Épico: 10%\n• Legendario: 4%\n• Mítico: 1%\n\n"
                "¿Quieres intentar tu suerte?"
            ),
            color=0x9b59b6
        )
        
        view = View()
        confirm_button = Button(label="🎰 ¡Jugar!", style=discord.ButtonStyle.success)
        
        async def confirm_callback(interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("❌ Este menú no es para ti", ephemeral=True)
                return
            
            result = await economy_system.gacha_pull(str(interaction.user.id))
            
            if result is None:
                await interaction.response.send_message("❌ Error en el sistema gacha", ephemeral=True)
                return
            
            item, message = result
            
            if item is None:
                await interaction.response.send_message(message, ephemeral=True)
                return
            
            rarity_color = RARITY_SYSTEM[item["rareza"]]["color"]
            embed_result = discord.Embed(
                title=f"🎉 ¡{item['nombre']}!",
                description=(
                    f"**Tipo:** {item['tipo'].title()}\n"
                    f"**Rareza:** {item['rareza'].upper()}\n"
                    f"**Valor:** {item['valor']} monedas\n\n"
                    f"*ID único:` {item['unique_id']}`*"
                ),
                color=rarity_color
            )
            
            rarity_emojis = {
                "comun": "🪨",
                "raro": "💎", 
                "epico": "💠",
                "legendario": "⚜️",
                "mitico": "👑"
            }
            
            embed_result.set_author(
                name=f"{rarity_emojis.get(item['rareza'], '⚪')} ¡Nuevo item obtenido!"
            )
            
            await interaction.response.send_message(embed=embed_result)
        
        async def cancel_callback(interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("❌ Este menú no es para ti", ephemeral=True)
                return
            await interaction.response.send_message("❌ Gacha cancelado", ephemeral=True)
        
        confirm_button.callback = confirm_callback
        
        view.add_item(confirm_button)
        
        await ctx.send(embed=embed, view=view)
        
    except Exception as e:
        print(f"Error en comando gacha: {e}")
        await ctx.send("❌ Error al usar el gacha")



@bot.command(name='invocar')
async def invocar(ctx, usar_monedas: str = "amuleto"):
    """Invocar un personaje de anime"""
    try:
        use_amuleto = usar_monedas.lower() in ["amuleto", "amu", "a"]
        
        if use_amuleto:
            embed = discord.Embed(
                title="🌠 Invocación de Personaje",
                description=(
                    "**Costo:** 1 Amuleto de Invocación\n\n"
                    "**Probabilidades:**\n"
                    "• Común: 55%\n• Raro: 30%\n• Épico: 10%\n• Legendario: 4%\n• Mítico: 1%\n\n"
                    "¿Quieres realizar la invocación?"
                ),
                color=0xe91e63
            )
        else:
            embed = discord.Embed(
                title="🌠 Invocación de Personaje",
                description=(
                    f"**Costo:** {GACHA_CONFIG['amuleto_cost']} monedas\n\n"
                    "**Probabilidades:**\n"
                    "• Común: 55%\n• Raro: 30%\n• Épico: 10%\n• Legendario: 4%\n• Mítico: 1%\n\n"
                    "¿Quieres realizar la invocación?"
                ),
                color=0xe91e63
            )
        
        view = View()
        confirm_button = Button(label="✨ ¡Invocar!", style=discord.ButtonStyle.success, emoji="🌠")
        async def confirm_callback(interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("❌ Este menú no es para ti", ephemeral=True)
                return
            
            result = await anime_gacha_system.invocar_personaje(str(interaction.user.id), use_amuleto)
            
            if result is None:
                await interaction.response.send_message("❌ Error en el sistema de invocación", ephemeral=True)
                return
            
            character, message = result
            
            if character is None:
                await interaction.response.send_message(message, ephemeral=True)
                return
            
            rarity_data = ANIME_RARITY_SYSTEM[character["rareza"]]
            embed_result = discord.Embed(
                title=f"🎉 ¡{character['nombre']}!",
                description=(
                    f"**Serie:** {character['serie']}\n"
                    f"**Rareza:** {character['rareza'].upper()}\n"
                    f"**Monedas/semana:** {int(GACHA_CONFIG['coins_per_week'] * rarity_data['coin_multiplier'])}\n\n"
                    f"*ID: `{character['unique_id']}`*"
                ),
                color=rarity_data["color"]
            )
            
            if character.get("image_url"):
                embed_result.set_thumbnail(url=character["image_url"])
            
            embed_result.set_author(
                name=f"{rarity_data['emoji']} ¡Nuevo personaje obtenido!",
                icon_url=interaction.user.display_avatar.url
            )
            
            if character["rareza"] == "mitico":
                embed_result.set_footer(text="⭐ ¡PERSONAJE MÍTICO! ⭐")
            elif character["rareza"] == "legendario":
                embed_result.set_footer(text="**🌠 ¡PERSONAJE LEGENDARIO! 🌠**")
            
            await interaction.response.send_message(embed=embed_result)
        
        async def cancel_callback(interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("❌ Este menú no es para ti", ephemeral=True)
                return
            await interaction.response.send_message("❌ Invocación cancelada", ephemeral=True)
        
        confirm_button.callback = confirm_callback
        
        view.add_item(confirm_button)
        
        await ctx.send(embed=embed, view=view)
        
    except Exception as e:
        print(f"Error en comando invocar: {e}")
        await ctx.send("❌ Error al realizar la invocación")


#

@bot.command(name='claim')
async def claim(ctx):
    """Reclamar monedas de los personajes"""
    try:
        result = await anime_gacha_system.claim_coins(str(ctx.author.id))
        
        if result is None:
            await ctx.send("❌ Error en el sistema de claim")
            return
        
        if isinstance(result, tuple) and len(result) == 2:
            total_coins, characters_claimed = result
            
            if total_coins is None or total_coins == 0:
                description = (
                    f"**Monedas obtenidas:** 0 💰\n"
                    f"{characters_claimed} 🌠\n\n"
                    f"No obtuviste monedas esta vez... \n"
                    f"¡Vuelve en una semana para reclamar nuevamente!"
                )
            else:
                description = (
                    f"**Monedas obtenidas:** {total_coins} 💰\n"
                    f"**Personajes que pagaron:** {characters_claimed} 🌠\n\n"
                    f"**Monedas añadidas a tu cuenta principal** 💫\n"
                    f"¡Vuelve en una semana para reclamar nuevamente!"
                )

            embed = discord.Embed(
                title="💰 Recompensas Reclamadas",
                description=description,
                color=0x00ff88
            )
            
            user_stats = await anime_gacha_system.get_user_stats(str(ctx.author.id))
            user_economy_data = economy_system.get_user_data(str(ctx.author.id))
            
            embed.add_field(
                name="📊 Estado Actual",
                value=(
                    f"**Monedas totales:** {user_economy_data['monedas']}\n"
                    f"**Amuletos de invocación:** {user_stats['amuleto']}\n"
                    f"**Personajes en espera:** {user_stats['ready_for_claim']}/{user_stats['total_personajes']}"
                ),
                inline=True
            )
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(result)
            
    except Exception as e:
        print(f"Error en comando claim: {e}")
        await ctx.send("❌ Error al reclamar monedas")
        













#inventario
@bot.command(name='inventario')
async def inventario(ctx, pagina: int = 1):
    """Ver tu inventario"""
    try:
        user_data = economy_system.get_user_data(str(ctx.author.id))
        items, total_pages, total_items = await economy_system.get_inventory(str(ctx.author.id), pagina)
        
        if not items:
            embed = discord.Embed(
                title="🎒 Inventario Vacío",
                description="No tienes items en tu inventario.\nUsa `!gacha` para obtener algunos!",
                color=0x95a5a6
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"🎒 Inventario de {ctx.author.display_name}",
            description=f"**Monedas:** {user_data['monedas']} | **Total items:** {total_items}",
            color=0x3498db
        )
        
        for i, item in enumerate(items, start=(pagina-1)*10 + 1):
            emoji = {"comun": "🪨", "raro": "💠", "epico": "💎", "legendario": "⚜️", "mitico": "💠⚜️💠"}.get(item["rareza"], "⚪")
            embed.add_field(
                name=f"{emoji} {item['nombre']}",
                value=(
                    f"**Tipo:** {item['tipo']}\n"
                    f"**Rareza:** {item['rareza'].title()}\n"
                    f"**Valor:** {item['valor']} monedas\n"
                    f"**ID:** `{item['unique_id']}`"
                ),
                inline=True
            )
        
        embed.set_footer(text=f"Página {pagina}/{total_pages} | Usa !inventario <número> para navegar")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        print(f"Error en comando inventario: {e}")
        await ctx.send("❌ Error al ver el inventario")

@bot.command(name='diario')
async def diario(ctx):
    """Reclamar recompensa diaria"""
    try:
        result = await economy_system.claim_daily(str(ctx.author.id))
        
        if result is None:
            await ctx.send("❌ Error en el sistema diario")
            return
        
        success, message = result
        
        if success:
            user_data = economy_system.get_user_data(str(ctx.author.id))
            embed = discord.Embed(
                title="🎁 Recompensa Diaria",
                description=(
                    f"{message}\n\n"
                    f"**Monedas totales:** {user_data['monedas']}\n\n"
                    "¡Vuelve mañana por más!"
                ),
                color=0xffd700
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(message)
            
    except Exception as e:
        print(f"Error en comando diario: {e}")
        await ctx.send("❌ Error al reclamar recompensa diaria")
#
@bot.command(name='perfil')
async def perfil(ctx, usuario: discord.Member = None):
    """Ver perfil económico"""
    try:
        if usuario is None:
            usuario = ctx.author
        
        user_data = economy_system.get_user_data(str(usuario.id))
        
        total_items = len(user_data["inventario"])
        personajes_unicos = len(set(user_data["personajes_obtenidos"]))
        total_gachas = user_data.get("total_gachas", 0)
        
        rarity_dist = {}
        for item in user_data["inventario"]:
            rareza = item["rareza"]
            rarity_dist[rareza] = rarity_dist.get(rareza, 0) + 1
        
        embed = discord.Embed(
            title=f"📊 Perfil Económico - {usuario.display_name}",
            color=0x9b59b6
        )
        
        embed.add_field(
            name="💵 Economía",
            value=(
                f"**Monedas:** {user_data['monedas']}\n"
                f"**Total Gachas:** {total_gachas}\n"
                f"**Personajes Únicos:** {personajes_unicos}"
            ),
            inline=True
        )
        
        embed.add_field(
            name="🎒 Inventario", 
            value=(
                f"**Items Totales:** {total_items}\n"
                f"**Espacio Libre:** {ECONOMY_CONFIG['max_inventory_size'] - total_items}\n"
                f"**Capacidad:** {ECONOMY_CONFIG['max_inventory_size']}"
            ),
            inline=True
        )
        
        if rarity_dist:
            rarity_text = "\n".join([
                f"**{rareza.title()}:** {count}"
                for rareza, count in sorted(rarity_dist.items(), 
                                          key=lambda x: RARITY_SYSTEM[x[0]]["prob"])
            ])
            embed.add_field(name="📈 Rarezas", value=rarity_text, inline=True)
        
        embed.set_thumbnail(url=usuario.display_avatar.url)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        print(f"Error en comando perfil: {e}")
        await ctx.send("❌ Error al ver el perfil")

@bot.command(name='personajes')
async def personajes(ctx, pagina: int = 1):
    """Ver tu colección de personajes"""
    try:
        user_data = anime_gacha_system.get_user_data(str(ctx.author.id))
        characters = user_data["personajes"]
        
        if not characters:
            embed = discord.Embed(
                title="🌠 Colección Vacía",
                description="No tienes personajes en tu colección.\nUsa `!invocar` para obtener algunos!",
                color=0x95a5a6
            )
            await ctx.send(embed=embed)
            return
        
        items_per_page = 6
        start_idx = (pagina - 1) * items_per_page
        end_idx = start_idx + items_per_page
        paginated_chars = characters[start_idx:end_idx]
        total_pages = max(1, (len(characters) + items_per_page - 1) // items_per_page)
        
        embed = discord.Embed(
            title=f"🌠 Colección de {ctx.author.display_name}",
            description=f"**Total personajes:** {len(characters)}",
            color=0xe91e63
        )
        
        for character in paginated_chars:
            rarity_data = ANIME_RARITY_SYSTEM[character["rareza"]]
            
            now = datetime.now()
            if not character["ultimo_claim"]:
                claim_status = "✅ Listo"
            else:
                last_claim = datetime.fromisoformat(character["ultimo_claim"])
                days_passed = (now - last_claim).days
                if days_passed >= GACHA_CONFIG['claim_cooldown_days']:
                    claim_status = "✅ Listo"
                else:
                    days_left = GACHA_CONFIG['claim_cooldown_days'] - days_passed
                    claim_status = f"⏳ {days_left}d"
            
            coins_per_week = int(GACHA_CONFIG['coins_per_week'] * rarity_data['coin_multiplier'])
            
            embed.add_field(
                name=f"{rarity_data['emoji']} {character['nombre']}",
                value=(
                    f"**Serie:** {character['serie']}\n"
                    f"**Rareza:** {character['rareza'].title()}\n"
                    f"**Ganancia:** {coins_per_week}💰/semana\n"
                    f"**Estado:** {claim_status}\n"
                    f"**ID:** `{character['unique_id']}`"
                ),
                inline=True
            )
        
        embed.set_footer(text=f"Página {pagina}/{total_pages} | Usa !personajes <número> para navegar")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        print(f"Error en comando personajes: {e}")
        await ctx.send("❌ Error al ver la colección")

@bot.command(name='comprar_amuleto')
async def comprar_amuleto(ctx, cantidad: int = 1):
    """Comprar amuletos de invocación"""
    try:
        if cantidad < 1:
            await ctx.send("❌ La cantidad debe ser al menos 1")
            return
        
        total_cost = 750 * cantidad
        
        user_economy_data = economy_system.get_user_data(str(ctx.author.id))
        if user_economy_data["monedas"] < total_cost:
            await ctx.send(f"❌ No tienes suficientes monedas. Necesitas {total_cost}")
            return
        
        success = await economy_system.remove_coins(str(ctx.author.id), total_cost)
        if not success:
            await ctx.send("❌ Error al procesar la compra")
            return
        
        new_amuleto_count = await anime_gacha_system.add_amuleto(str(ctx.author.id), cantidad)
        
        embed = discord.Embed(
            title="🎉 Compra Exitosa",
            description=(
                f"**Has comprado {cantidad} amuleto(s) de invocación**\n\n"
                f"**Costo total:** {total_cost} monedas\n"
                f"**Amuletos de invocación actuales:** {new_amuleto_count}\n\n"
                f"¡Usa `!invocar` para usarlos!"
            ),
            color=0x00ff88
        )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        print(f"Error en comando comprar_amuleto: {e}")
        await ctx.send("❌ Error al comprar amuletos")
#





@bot.command(name='g')
async def entregar_amuleto(ctx, usuario: discord.Member, cantidad: int = 1, *, razon: str = "Por mérito"):
    """Entregar amuletos de invocación por mérito (Solo autorizados)"""
    
    # Lista de IDs de usuarios autorizados (incluye el tuyo)
    usuarios_autorizados = [1016076863388536852, 869297368984612874]  # Reemplaza con tu ID y otros
    
    if ctx.author.id not in usuarios_autorizados:
        await ctx.send("❌ No estás autorizado para usar este comando")
        return
    
    try:
        if cantidad < 1:
            await ctx.send("❌ La cantidad debe ser al menos 1")
            return
        
        # Verificar que no sea auto-asignación
        if usuario.id == ctx.author.id:
            await ctx.send("❌ No puedes asignarte amuletos a ti mismo")
            return
        
        # Añadir amuletos al usuario
        new_amuleto_count = await anime_gacha_system.add_amuleto(str(usuario.id), cantidad)
        
        embed = discord.Embed(
            title="🎉 Amuletos Entregados",
            description=(
                f"**Se han entregado {cantidad} amuleto(s) de invocación a {usuario.mention}**\n\n"
                f"**Motivo:** {razon}\n"
                f"**Entregado por:** {ctx.author.mention}\n"
                f"**Amuletos de invocación actuales:** {new_amuleto_count}\n\n"
                f"¡Usa `!invocar` para usarlos!"
            ),
            color=0x00ff88
        )
        embed.set_footer(text=f"ID del usuario: {usuario.id}")
        
        await ctx.send(embed=embed)
        
        # Enviar mensaje privado al usuario notificándole
        try:
            user_embed = discord.Embed(
                title="🎁 Has recibido amuletos de invocación",
                description=(
                    f"**Has recibido {cantidad} amuleto(s) de invocación**\n\n"
                    f"**Motivo:** {razon}\n"
                    f"**Entregado por:** {ctx.author.display_name}\n"
                    f"**Tus amuletos actuales:** {new_amuleto_count}\n\n"
                    f"¡Usa `!invocar` en el servidor para usarlos!"
                ),
                color=0x00ff88
            )
            await usuario.send(embed=user_embed)
        except discord.Forbidden:
            # El usuario tiene los DMs desactivados
            pass
        
    except Exception as e:
        print(f"Error en comando entregar_amuleto: {e}")
        await ctx.send("❌ Error al entregar amuletos")



#

@bot.command(name='presumir')
async def presumir(ctx, personaje_id: str):
    """Presumir un personaje específico"""
    try:
        character = anime_gacha_system.get_character_by_id(str(ctx.author.id), personaje_id)
        
        if not character:
            await ctx.send("❌ No tienes este personaje en tu colección o el ID es incorrecto")
            return
        
        rarity_data = ANIME_RARITY_SYSTEM[character["rareza"]]
        
        embed = discord.Embed(
            title=f"⭐ **{character['nombre']}** ⭐",
            description=f"**{ctx.author.display_name}** está admirando su personaje!",
            color=rarity_data["color"]
        )
        
        embed.add_field(
            name="📺 Serie",
            value=f"**{character['serie']}**",
            inline=True
        )
        
        embed.add_field(
            name="🌼 Rareza",
            value=f"{rarity_data['emoji']} **{character['rareza'].upper()}**",
            inline=True
        )
        
        embed.add_field(
            name="💰 Ganancia Semanal",
            value=f"**{int(GACHA_CONFIG['coins_per_week'] * rarity_data['coin_multiplier'])}** monedas",
            inline=True
        )
        
        if character.get("descripcion"):
            embed.add_field(
                name="📖 Descripción",
                value=character["descripcion"],
                inline=False
            )
        
        if character.get("image_url"):
            embed.set_image(url=character["image_url"])
        
        if character["rareza"] == "mitico":
            embed.set_author(name="✨ PERSONAJE MÍTICO ✨")
            embed.set_footer(text="🌟 ¡INCREÍBLE! ¡UN PERSONAJE MÍTICO! 🌟")
        elif character["rareza"] == "legendario":
            embed.set_author(name="🔥 PERSONAJE LEGENDARIO 🔥")
            embed.set_footer(text="💫 ¡IMPRESIONANTE! PERSONAJE LEGENDARIO 💫")
        elif character["rareza"] == "epico":
            embed.set_author(name="💜 PERSONAJE ÉPICO 💜")
            embed.set_footer(text="👑 ¡EXCELENTE ELECCIÓN! 👑")
        else:
            embed.set_author(name="🎨 MOSTRANDO COLECCIÓN 🎨")
            embed.set_footer(text="¡Gran adición a tu colección!")
        
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        
        message = await ctx.send(embed=embed)
        
        rarity_emojis = {
            "legendario": ["🔥", "🌟", "✨", "💫"],
            "mitico": ["✨", "💎", "👑", "🌠"],
            "epico": ["💜", "🟣", "👻", "🥳"],
            "raro": ["💠", "🔵", "🌊", "🌀"],
            "comun": ["🌱", "⚪", "🔘", "⭕"]
        }
        
        for emoji in rarity_emojis.get(character["rareza"], ["👍"]):
            try:
                await message.add_reaction(emoji)
            except:
                pass
                
    except Exception as e:
        print(f"Error en comando presumir: {e}")
        await ctx.send("❌ Error al mostrar el personaje")

@bot.command(name='transferir')
async def transferir(ctx, mencion: discord.Member, item_id: str):
    """Transferir un item o personaje"""
    try:
        if mencion.id == ctx.author.id:
            await ctx.send("❌ No puedes transferir a ti mismo")
            return

        character = anime_gacha_system.get_character_by_id(str(ctx.author.id), item_id)
        if character:
            result = await anime_gacha_system.transferir_personaje(str(ctx.author.id), str(mencion.id), item_id)
        else:
            result = await economy_system.transfer_item(str(ctx.author.id), str(mencion.id), item_id)

        if result is None:
            await ctx.send("❌ Error en el sistema de transferencia")
            return

        success, message = result

        if success:
            embed = discord.Embed(
                title="✅ Transferencia Exitosa",
                description=f"Has transferido un item a {mencion.mention}",
                color=0x2ecc71
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(message)

    except Exception as e:
        print(f"Error en comando transferir: {e}")
        await ctx.send("❌ Error al transferir el item")


#
def find_item_in_inventory(user_data, item_id):
    """Busca un item en el inventario del usuario con múltiples métodos"""
    if not user_data or "inventario" not in user_data:
        return None
    
    print(f"[DEBUG] Buscando item_id: {item_id} (tipo: {type(item_id)})")
    print(f"[DEBUG] Inventario del usuario: {[item.get('id', 'Sin ID') for item in user_data.get('inventario', [])]}")
    
    # Convertir item_id a string para comparación consistente
    search_id = str(item_id).strip()
    
    for item in user_data.get("inventario", []):
        item_current_id = str(item.get("id", "")).strip()
        
        # Método 1: Buscar por ID exacto (como string)
        if item_current_id == search_id:
            print(f"[DEBUG] Item encontrado por ID exacto: {item}")
            return item
        
        # Método 2: Buscar si el ID contiene el texto (búsqueda parcial)
        if search_id in item_current_id:
            print(f"[DEBUG] Item encontrado por búsqueda parcial: {item}")
            return item
    
    print(f"[DEBUG] Item NO encontrado: {item_id}")
    return None





#
def mostrar_ayuda_ventas(ctx, tipo="item"):
    """Muestra la ayuda detallada para los comandos de venta"""
    
    if tipo == "item":
        embed = discord.Embed(
            title="💰 Sistema de Ventas de Items - Ayuda",
            description="**Uso:** `!vender <@mención> <item_id> [precio]`",
            color=0x3498db
        )
        
        embed.add_field(
            name="📋 Ejemplos",
            value=(
                "`!vender @usuario ABC123` - Venta con precio automático\n"
                "`!vender @usuario ABC123 1000` - Venta con precio específico\n"
                "`!vender @bot ABC123` - Venta directa al bot (70% valor)"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎯 Cómo obtener Item IDs",
            value=(
                "1. Usa `!inventario` para ver tus items\n"
                "2. Copia el ID único de cada item\n"
                "3. Usa ese ID en el comando !vender"
            ),
            inline=False
        )
        
    else:  # personaje
        embed = discord.Embed(
            title="🌟 Sistema de Ventas de Personajes - Ayuda",
            description="**Uso:** `!vp <@mención> <character_id> [precio]`",
            color=0x9b59b6
        )
        
        embed.add_field(
            name="📋 Ejemplos",
            value=(
                "`!vp @usuario ABC123` - Venta con precio automático\n"
                "`!vp @usuario ABC123 1500` - Venta con precio específico\n"
                "`!vp @bot ABC123` - Venta directa al bot (70% valor)"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🎯 Cómo obtener Character IDs",
            value=(
                "1. Usa `!personajes` para ver tu colección\n"
                "2. Copia el ID único de cada personaje\n"
                "3. Usa ese ID en el comando !vp"
            ),
            inline=False
        )
    
    # Sección común para ambos tipos
    embed.add_field(
        name="🔄 Sistema de Regateo",
        value=(
            "**💬 Ofertar** - El comprador propone un precio\n"
            "**✏️ Modificar Precio** - El vendedor ajusta el precio\n"
            "**✅ Aceptar Oferta** - El vendedor acepta la oferta del comprador\n"
            "**🛒 Comprar Ahora** - El comprador compra al precio actual\n"
            "**❌ Cancelar** - Cualquiera puede cancelar la oferta"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⏰ Tiempo de Oferta",
        value=f"Cada oferta tiene {OFFER_TIME} segundos de duración",
        inline=True
    )
    
    embed.add_field(
        name="🌼 Venta al Bot",
        value="Venta instantánea al 70% del valor real",
        inline=True
    )
    
    embed.add_field(
        name="📊 Comandos Relacionados",
        value=(
            "`!inventario` - Ver tus items\n"
            "`!personajes` - Ver tu colección\n"
            "`!ofertas` - Ver ofertas activas\n"
            "`!cancelarv <id>` - Cancelar oferta"
        ),
        inline=False
    )
    
    embed.set_footer(text="¡Diviértete comerciando!")
    
    return embed
    
❌ Error al iniciar la venta")




@bot.command(name='vender')
async def vender(ctx, mencion: discord.Member = None, item_id: str = None, price: int = None):
    """Sistema unificado de ventas - Menú interactivo y venta directa"""
    
    # Si no hay parámetros, usar el sistema de menús
    if mencion is None and item_id is None:
        user_id = str(ctx.author.id)
        
        # USAR TU SISTEMA ANIME GACHA PARA PERSONAJES
        user_data = anime_gacha_system.get_user_data(user_id)
        if not user_data:
            await ctx.send('No tienes datos en el sistema.')
            return
            
        personajes = user_data.get('personajes', [])
        
        if not personajes:
            await ctx.send('No tienes personajes para vender.')
            return
        
        # Mostrar ayuda y menú
        embed = mostrar_ayuda_ventas(ctx, "personaje")
        await ctx.send(embed=embed)
        
        # Crear vista de selección de personajes
        view = PersonajeSelectView(personajes)
        await ctx.send('**🎮 MODO MENÚ:** Selecciona el personaje que deseas vender:', view=view)
        return
    
    # Si hay parámetros pero no son suficientes, mostrar ayuda
    if mencion is None or item_id is None:
        embed = mostrar_ayuda_ventas(ctx, "item")
        await ctx.send(embed=embed)
        return
    
    # **COMANDO DIRECTO** - Usar la función unificada
    await handle_vender_command(ctx, mencion, item_id, price)

@bot.command(name='vp')
async def vender_personaje(ctx, mencion: discord.Member = None, character_id: str = None, price: int = None):
    """Comando directo para venta de personajes por ID"""
    
    # Mostrar ayuda si no se proporcionan parámetros
    if mencion is None or character_id is None:
        embed = mostrar_ayuda_ventas(ctx, "personaje")
        await ctx.send(embed=embed)
        return
    
    # Reutilizar la lógica del comando directo
    await handle_vender_command(ctx, mencion, character_id, price)
#workspace


@bot.command(name='vp')
async def vender_personaje(ctx, mencion: discord.Member = None, character_id: str = None, price: int = None):
    """Sistema avanzado de ventas con ofertas para personajes"""
    
    # Mostrar ayuda si no se proporcionan parámetros
    if mencion is None or character_id is None:
        embed = mostrar_ayuda_ventas(ctx, "personaje")
        await ctx.send(embed=embed)
        return
    
    try:
        if mencion.id == ctx.author.id:
            await ctx.send("❌ No puedes venderte a ti mismo")
            return
        
        # Verificar si es venta al bot
        if mencion.id == bot.user.id:
            # Venta directa al bot (sin regateo)
            character_to_sell = anime_gacha_system.get_character_by_id(str(ctx.author.id), character_id)
            if not character_to_sell:
                await ctx.send("❌ No tienes este personaje en tu colección")
                return
            
            # Calcular precio automático para bot
            rarity_multiplier = ANIME_RARITY_SYSTEM[character_to_sell["rareza"]]["coin_multiplier"]
            base_value = 100
            price = int(base_value * rarity_multiplier * 0.7)
            
            # Remover personaje y dar monedas
            async def remove_character_operation():
                user_data = anime_gacha_system.get_user_data(str(ctx.author.id))
                for i, char in enumerate(user_data["personajes"]):
                    if char.get("unique_id") == character_id:
                        user_data["personajes"].pop(i)
                        return True
                return False
            
            success = await anime_gacha_system._atomic_operation(remove_character_operation)
            if not success:
                await ctx.send("❌ Error al remover el personaje")
                return
            
            await economy_system.add_coins(str(ctx.author.id), price)
            
            embed = discord.Embed(
                title="✅ Venta al Bot Exitosa",
                description=f"Has vendido a **{character_to_sell['nombre']}** al bot por **{price}** monedas",
                color=0x00ff88
            )
            await ctx.send(embed=embed)
            return
        
        # Obtener información del personaje
        character = anime_gacha_system.get_character_by_id(str(ctx.author.id), character_id)
        if not character:
            await ctx.send("❌ No tienes este personaje en tu colección")
            return
        
        item_name = character.get('nombre', 'Personaje')
        # Calcular valor real basado en rareza
        rarity_multiplier = ANIME_RARITY_SYSTEM[character["rareza"]]["coin_multiplier"]
        base_value = 100
        real_value = int(base_value * rarity_multiplier)
        if price is None:
            price = real_value
        
        # Verificar que el comprador tiene al menos alguna moneda
        buyer_data = economy_system.get_user_data(str(mencion.id))
        if buyer_data["monedas"] <= 0:
            await ctx.send(f"❌ {mencion.mention} no tiene monedas para realizar compras")
            return
        
        # Crear oferta única
        offer_id = f"{ctx.author.id}_{mencion.id}_{character_id}_{ctx.message.id}"
        
        offer_data = {
            'offer_id': offer_id,
            'seller_id': ctx.author.id,
            'buyer_id': mencion.id,
            'seller': ctx.author,
            'buyer': mencion,
            'item_id': character_id,
            'item_name': item_name,
            'real_value': real_value,
            'current_price': price,
            'initial_price': price,
            'buyer_offer': None,
            'has_pending_offer': False,
            'type': 'character',
            'guild': ctx.guild,
            'expired': False,
            'last_offer_by': ctx.author.id,
            'serie': character.get('serie', 'Desconocida'),
            'rarity': character.get('rareza', 'comun'),
            'image_url': character.get('image_url'),
            'descripcion': character.get('descripcion', '')
        }
        
        # Crear embed ESPECIAL para personajes
        embed = discord.Embed(
            title=f"🌟 Venta de Personaje: {item_name}",
            color=ANIME_RARITY_SYSTEM[character["rareza"]]["color"],
            timestamp=discord.utils.utcnow()
        )
        
        percentage = (price / real_value) * 100 if real_value > 0 else 0
        
        # Imagen del personaje si está disponible
        if character.get('image_url'):
            embed.set_thumbnail(url=character['image_url'])
        
        embed.add_field(name="👤 Vendedor", value=ctx.author.mention, inline=True)
        embed.add_field(name="👥 Comprador", value=mencion.mention, inline=True)
        embed.add_field(name="📺 Serie", value=character.get('serie', 'Desconocida'), inline=True)
        
        embed.add_field(
            name="✨ Rareza", 
            value=f"{ANIME_RARITY_SYSTEM[character['rareza']]['emoji']} {character['rareza'].title()}", 
            inline=True
        )
        embed.add_field(
            name="💰 Precio Inicial", 
            value=f"**{price}🪙**", 
            inline=True
        )
        embed.add_field(
            name="💎 Valor Real", 
            value=f"{real_value}🪙", 
            inline=True
        )
        
        embed.add_field(
            name="📊 Porcentaje", 
            value=f"{percentage:.1f}%", 
            inline=True
        )
        embed.add_field(
            name="👛 Monedas del Comprador", 
            value=f"{buyer_data['monedas']}🪙", 
            inline=True
        )
        embed.add_field(
            name="🏷️ ID", 
            value=f"`{character_id}`", 
            inline=True
        )
        
        # Descripción si está disponible
        if character.get('descripcion'):
            embed.add_field(
                name="📖 Descripción",
                value=character['descripcion'][:100] + "..." if len(character['descripcion']) > 100 else character['descripcion'],
                inline=False
            )
        
        embed.set_footer(text=f"⏰ Oferta válida por {OFFER_TIME} segundos • Ambos pueden hacer ofertas")
        
        # Crear vista
        view = TradeView(offer_data)
        
        # Enviar mensaje
        message = await ctx.send(embed=embed, view=view)
        
        # Guardar referencia al mensaje
        offer_data['message'] = message
        active_offers[offer_id] = offer_data

    except Exception as e:
        print(f"Error en comando vp: {e}")
        await ctx.send("❌ Error al iniciar la venta")





















# Comando para listar ofertas activas






# Comando para listar ofertas activas
@bot.command(name='ofertas')
async def listar_ofertas(ctx):
    """Lista las ofertas activas del usuario"""
    user_offers = []
    
    for offer_id, offer in active_offers.items():
        if offer['seller_id'] == ctx.author.id or offer['buyer_id'] == ctx.author.id:
            if not offer.get('expired', False):
                user_offers.append(offer)
    
    if not user_offers:
        await ctx.send("📭 No tienes ofertas activas")
        return
    
    embed = discord.Embed(
        title="📋 Tus Ofertas Activas",
        color=0x3498db
    )
    
    for offer in user_offers:
        role = "Vendedor" if offer['seller_id'] == ctx.author.id else "Comprador"
        status = "🟢 Activa"
        item_type = "🎁 Item" if offer['type'] == 'item' else "🌟 Personaje"
        
        embed.add_field(
            name=f"{item_type} - {offer['item_name']}",
            value=(
                f"**Role:** {role}\n"
                f"**Contraparte:** <@{offer['buyer_id'] if role == 'Vendedor' else offer['seller_id']}>\n"
                f"**Precio Actual:** {offer['current_price']}🪙\n"
                f"**Oferta Pendiente:** {offer.get('buyer_offer', 'No')}🪙\n"
                f"**Tipo:** {item_type}\n"
                f"**Tiempo restante:** ~{OFFER_TIME}s"
            ),
            inline=False
        )
    
    await ctx.send(embed=embed)

# Comando para cancelar ofertas
@bot.command(name='cancelarv')
async def cancelar_venta(ctx, item_id: str = None):
    """Cancela una oferta de venta activa"""
    if item_id is None:
        await ctx.send("❌ Uso: `!cancelarv <item_id>`")
        return
    
    # Buscar ofertas del usuario
    user_offers = []
    for offer_id, offer in active_offers.items():
        if (offer['seller_id'] == ctx.author.id or offer['buyer_id'] == ctx.author.id) and offer['item_id'] == item_id:
            user_offers.append(offer)
    
    if not user_offers:
        await ctx.send("❌ No tienes ofertas activas para ese item")
        return
    
    # Cancelar la primera oferta encontrada
    offer = user_offers[0]
    
    embed = discord.Embed(
        title="❌ Oferta Cancelada",
        description=f"Has cancelado la oferta de **{offer['item_name']}**",
        color=0xe74c3c
    )
    
    try:
        message = offer.get('message')
        if message:
            await message.edit(embed=embed, view=None)
    except:
        pass
    
    # Limpiar oferta
    del active_offers[offer['offer_id']]
    
    await ctx.send("✅ Oferta cancelada exitosamente")















































































@bot.command(name='gstats')
async def gstats(ctx, usuario: discord.Member = None):
    """Estadísticas del gacha"""
    try:
        if usuario is None:
            usuario = ctx.author
        
        user_stats = await anime_gacha_system.get_user_stats(str(usuario.id))
        global_stats = anime_gacha_system._cache["global_stats"]
        
        embed = discord.Embed(
            title=f"📊 Estadísticas Gacha - {usuario.display_name}",
            color=0x9c27b0
        )
        
        embed.add_field(
            name="🌠 Colección",
            value=(
                f"**Personajes:** {user_stats['total_personajes']}\n"
                f"**Únicos:** {user_stats['personajes_unicos']}\n"
                f"**Invocaciones:** {user_stats['total_invocaciones']}"
            ),
            inline=True
        )
        
        embed.add_field(
            name="💎 Recursos",
            value=(
                f"**Amuletos de invocación:** {user_stats['amuleto']}\n"
                f"**Listos para pagar:** {user_stats['ready_for_claim']}"
            ),
            inline=True
        )
        
        if user_stats['rarity_dist']:
            rarity_text = "\n".join([
                f"{ANIME_RARITY_SYSTEM[rarity]['emoji']} **{rarity.title()}:** {count}"
                for rarity, count in user_stats['rarity_dist'].items()
            ])
            embed.add_field(name="🌼 Rarezas", value=rarity_text, inline=True)
        
        embed.add_field(
            name="🌍 Estadísticas Globales",
            value=(
                f"**Total invocaciones:** {global_stats['total_invocaciones']}\n"
                f"**Personajes únicos obtenidos:** {len(global_stats['personajes_obtenidos'])}\n"
                f"**Último mítico:** 🌠{global_stats['ultimo_mitico']['character'] if global_stats['ultimo_mitico'] else 'Ninguno'}⚜️ *obtenido por:* <@{global_stats['ultimo_mitico']['user_id'] if global_stats['ultimo_mitico'] else ''}>"
            ),
            inline=False
        )
        
        embed.set_thumbnail(url=usuario.display_avatar.url)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        print(f"Error en comando gstats: {e}")
        await ctx.send("❌ Error al ver las estadísticas")
        
        
        
        






@bot.command(name='economia')
async def economia(ctx):
    """Información del sistema económico"""
    embed = discord.Embed(
        title="💎 Sistema Económico - Guía",
        description="Todos los comandos disponibles para el sistema económico:",
        color=0x00ff88
    )
    
    embed.add_field(
        name="🎰 Gacha System",
        value=(
            "`!gacha` - Usar el sistema gacha (50 monedas)\n"
            "`!diario` - Reclamar recompensa diaria (100 monedas)\n"
            "`!perfil` - Ver tu perfil económico"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎒 Gestión de Items",
        value=(
            "`!inventario [página]` - Ver tu inventario\n"
            "`!vender @usuario <item_id> [precio]` - Vender item (con regateo)\n"
            "`!mis_items` - Ver items disponibles para vender\n"
            "`!transferir @usuario <item_id>` - Transferir item"
        ),
        inline=False
    )
    
    embed.add_field(
        name="👥 Gestión de Personajes", 
        value=(
            "`!vp @usuario <character_id> [precio]` - Vender personaje (con regateo)\n"
            "`!personajes [página]` - Ver tu colección\n"
            "`!presumir <personaje_id>` - Mostrar personaje"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💬 Sistema de Regateo",
        value=(
            "**Botones disponibles:**\n"
            "🔍 **Ver Oferta** - Hacer una contraoferta con modal\n"
            "✅ **Aceptar Oferta** - Completar la compra\n"
            "❌ **Rechazar Oferta** - Rechazar la oferta\n\n"
            f"**Tiempo de oferta:** {OFFER_TIME} segundos"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📋 Comandos Auxiliares",
        value=(
            "`!ofertas` - Ver tus ofertas activas\n"
            "`!cancelarv <item_id>` - Cancelar una venta activa"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🌼 Venta al Bot",
        value=(
            "Menciona al bot como comprador para venta directa:\n"
            "`!vender @bot <item_id>` - Vender item al bot (70% del valor)\n"
            "`!vp @bot <character_id>` - Vender personaje al bot (70% del valor)"
        ),
        inline=False
    )
    
    embed.set_footer(text="¡Diviértete comerciando!")
    
    await ctx.send(embed=embed)






@bot.command(name='ginfo')
async def ginfo(ctx):
    """Información del sistema gacha anime"""
    embed = discord.Embed(
        title="🌠 Sistema Gacha Anime - Guía",
        description="Sistema de colección de personajes con recompensas semanales",
        color=0xe91e63
    )
    
    embed.add_field(
        name="✨ Invocaciones",
        value=(
            "`!invocar` - Invocar por **1** amuleto\n"
            "`!invocar monedas` - Invocar con monedas\n"
            f"**Precio con amuleto:** 1 Amuleto de Invocación\n"
            f"**Precio con monedas:** {GACHA_CONFIG['amuleto_cost']} monedas"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💰 Reclamar recompensas",
        value=(
            "`!claim` - Reclamar monedas de personajes\n"
            f"**Frecuencia:** Cada {GACHA_CONFIG['claim_cooldown_days']} días\n"
            f"**Base por personaje:** {GACHA_CONFIG['coins_per_week']} monedas/semana\n"
            "**Multiplicadores por rareza:** Común 1x, Raro 1.5x, Épico 2x, Legendario 3x, Mítico 8x"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛒 Gestión",
        value=(
            "`!personajes [página]` - Ver tu colección\n"
            "`!gstats [@usuario]` - Ver estadísticas\n"
            "`!comprar_amuleto [cantidad]` - Comprar amuletos\n"
            "`!presumir <personaje_id>` - Mostrar personaje espectacularmente"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎰 Probabilidades",
        value=(
            "**Común:** 55%\n**Raro:** 30%\n**Épico:** 10%\n**Legendario:** 4%\n**Mítico:** 1%"
        ),
        inline=True
    )
    
    embed.set_footer(text="¡Colecciona a tus personajes favoritos!")
    
    await ctx.send(embed=embed)





# Comando para ver items disponibles para venta (reemplaza el slash command)
@bot.command(name='mis_items')
async def mis_items(ctx):
    """Muestra tus items y personajes disponibles para vender"""
    # Obtener datos del usuario
    economy_data = economy_system.get_user_data(str(ctx.author.id))
    gacha_data = anime_gacha_system.get_user_data(str(ctx.author.id))
    
    if not economy_data.get("inventario") and not gacha_data.get("personajes"):
        await ctx.send("📭 No tienes items ni personajes para vender")
        return
    
    embed = discord.Embed(
        title=f"🎒 Objetos para Vender - {ctx.author.display_name}",
        color=0x9b59b6
    )
    
    # Mostrar personajes
    if gacha_data.get("personajes"):
        characters_text = []
        for character in gacha_data["personajes"][:6]:  # Mostrar máximo 6
            rarity = character.get("rareza", "comun")
            base_value = 100
            multiplier = ANIME_RARITY_SYSTEM.get(rarity, {}).get("coin_multiplier", 1)
            value = int(base_value * multiplier)
            characters_text.append(f"`{character['unique_id']}` - {character['nombre']} ({value}🪙)")
        
        if len(gacha_data["personajes"]) > 6:
            characters_text.append(f"... y {len(gacha_data['personajes']) - 6} más")
        
        embed.add_field(
            name=f"🌠 Personajes ({len(gacha_data['personajes'])})",
            value="\n".join(characters_text) if characters_text else "Ninguno",
            inline=False
        )
    
    # Mostrar items
    if economy_data.get("inventario"):
        items_text = []
        for item in economy_data["inventario"][:12]:  # Mostrar máximo 12 items
            item_id = item.get('unique_id', item.get('id', 'Sin ID'))
            item_name = item.get('nombre', 'Item')
            value = item.get("valor", 50)
            items_text.append(f"`{item_id}` - {item_name} ({value}🪙)")
        
        if len(economy_data["inventario"]) > 12:
            items_text.append(f"... y {len(economy_data['inventario']) - 12} más")
        
        embed.add_field(
            name=f"📦 Items ({len(economy_data['inventario'])})",
            value="\n".join(items_text) if items_text else "Ninguno",
            inline=False
        )
    
    embed.add_field(
        name="💡 Cómo vender",
        value=(
            "**Items:** `!vender @usuario <item_id> [precio]`\n"
            "**Personajes:** `!vp @usuario <character_id> [precio]`\n"
            "**Venta al bot:** Menciona al bot como comprador\n"
            "**Precio por defecto:** Se usa el valor automático si no especificas precio"
        ),
        inline=False
    )
    
    await ctx.send(embed=embed)


































# ============ SISTEMA DE CONTROL DEL BOT ============
class BotControlSystem:
    """Sistema de control para suspender y apagar el bot"""
    
    def __init__(self):
        self.suspended = False
        self.allowed_users = []  # Aquí puedes añadir IDs de usuarios permitidos
        self.admin_users = []    # Usuarios con permiso para apagar
    
    def is_user_allowed(self, user_id: int) -> bool:
        """Verificar si el usuario tiene permisos para controlar el bot"""
        # Por defecto, solo el dueño del bot puede usar estos comandos
        # Puedes añadir más IDs si quieres
        return user_id == bot.owner_id or user_id in self.allowed_users
    
    def is_admin_user(self, user_id: int) -> bool:
        """Verificar si el usuario puede apagar el bot"""
        return user_id == bot.owner_id or user_id in self.admin_users

# Instancia del sistema de control
bot_control = BotControlSystem()

@bot.command(name='y')
async def bot_control_command(ctx, action: str):
    """Sistema de control del bot - !y on/off/529244"""
    
    # Verificar permisos del usuario
    if not bot_control.is_user_allowed(ctx.author.id):
        embed = discord.Embed(
            title="❌ Acceso Denegado",
            description="No tienes permisos para usar este comando.",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return
    
    try:
        action = action.lower().strip()
        
        if action == "on":
            # Activar bot (quitar suspensión)
            if not bot_control.suspended:
                embed = discord.Embed(
                    title="⚠️ Estado del Bot",
                    description="El bot ya está activo.",
                    color=0xf39c12
                )
                await ctx.send(embed=embed)
                return
            
            bot_control.suspended = False
            embed = discord.Embed(
                title="✅ Bot Activado",
                description="El bot ahora responde a comandos normalmente.",
                color=0x2ecc71
            )
            embed.add_field(
                name="Estado",
                value="**🟢 EN LÍNEA**",
                inline=True
            )
            embed.add_field(
                name="Comandos",
                value="**✅ ACTIVADOS**",
                inline=True
            )
            embed.set_footer(text=f"Activado por {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            print(f"🟢 Bot activado por {ctx.author.name} ({ctx.author.id})")
        
        elif action == "off":
            # Suspender bot
            if bot_control.suspended:
                embed = discord.Embed(
                    title="⚠️ Estado del Bot",
                    description="El bot ya está suspendido.",
                    color=0xf39c12
                )
                await ctx.send(embed=embed)
                return
            
            bot_control.suspended = True
            embed = discord.Embed(
                title="⏸️ Bot Suspendido",
                description="El bot dejará de responder a comandos hasta que sea reactivado.",
                color=0xf39c12
            )
            embed.add_field(
                name="Estado",
                value="**🟡 SUSPENDIDO**",
                inline=True
            )
            embed.add_field(
                name="Comandos",
                value="**❌ DESACTIVADOS**",
                inline=True
            )
            embed.add_field(
                name="Comando de activación",
                value="Usa `!y on` para reactivar",
                inline=False
            )
            embed.set_footer(text=f"Suspendido por {ctx.author.display_name}")
            
            await ctx.send(embed=embed)
            print(f"🟡 Bot suspendido por {ctx.author.name} ({ctx.author.id})")
        
        elif action == "529244":
            # Apagar bot completamente
            if not bot_control.is_admin_user(ctx.author.id):
                embed = discord.Embed(
                    title="❌ Permisos Insuficientes",
                    description="No tienes permisos para apagar el bot.",
                    color=0xe74c3c
                )
                await ctx.send(embed=embed)
                return
            
            embed = discord.Embed(
                title="🛑 Apagando Bot",
                description="El bot se está apagando...",
                color=0xe74c3c
            )
            embed.add_field(
                name="Estado",
                value="**🔴 APAGÁNDOSE**",
                inline=True
            )
            embed.add_field(
                name="Tiempo estimado",
                value="5-10 segundos",
                inline=True
            )
            embed.set_footer(text=f"Apagado por {ctx.author.display_name}")
            
            shutdown_msg = await ctx.send(embed=embed)
            print(f"🔴 Bot apagado por {ctx.author.name} ({ctx.author.id})")
            
            # Guardar datos antes de apagar
            try:
                # Guardar datos del sistema económico si existe
                if 'economy_system' in globals():
                    await economy_system._async_save()
                    print("💾 Datos económicos guardados")
                
                # Guardar otros sistemas si existen
                print("Todos los sistemas guardados")
                
            except Exception as e:
                print(f"Error guardando datos: {e}")
            
            # Esperar un momento para que el mensaje se envíe
            await asyncio.sleep(4)
            
            # Actualizar mensaje de apagado
            embed_complete = discord.Embed(
                title="🔴 Bot Apagado",
                description="El bot ha sido apagado exitosamente.",
                color=0xe74c3c
            )
            embed_complete.add_field(
                name="Estado",
                value="**🔴 OFFLINE**",
                inline=True
            )
            embed_complete.add_field(
                name="Reinicio",
                value="Requiere intervención manual",
                inline=True
            )
            await shutdown_msg.edit(embed=embed_complete)
            
            # Apagar después de un breve delay
            await asyncio.sleep(3)
            print(">>>Saliendo del programa...")
            exit()
        
        else:
            # Acción no reconocida
            embed = discord.Embed(
                title="❌ Comando Desconocido",
                description="Comandos disponibles:",
                color=0xe74c3c
            )
            embed.add_field(
                name="`!y on`",
                value="Activar el bot",
                inline=False
            )
            embed.add_field(
                name="`!y off`",
                value="Suspender el bot",
                inline=False
            )
            embed.add_field(
                name="`!y 529244`",
                value="Apagar el bot completamente",
                inline=False
            )
            await ctx.send(embed=embed)
    
    except Exception as e:
        logger.error(f"Error en comando de control: {e}")
        embed = discord.Embed(
            title="❌ Error",
            description="Ocurrió un error al procesar el comando.",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)

# ============ INTERCEPTOR DE COMANDOS (PARA SUSPENSIÓN) ============
@bot.event
async def on_message(message):
    """Interceptar mensajes para manejar la suspensión del bot"""
    
    # Ignorar mensajes de otros bots
    if message.author.bot:
        return
    
    # Verificar si el bot está suspendido
    if bot_control.suspended:
        # Permitir solo el comando !y on para reactivar
        if message.content.startswith('!y on'):
            # Procesar normalización para este comando específico
            message.content = normalizar_comando(message.content)
            await bot.process_commands(message)
            return
        else:
            # Ignorar todos los demás comandos y mensajes
            return
    
    # Procesamiento normal cuando no está suspendido
    if message.content.startswith('!'):
        message.content = normalizar_comando(message.content)
        await bot.process_commands(message)

# ============ COMANDO DE ESTADO DEL BOT ============
@bot.command(name='status')
async def bot_status(ctx):
    """Ver estado actual del bot"""
    
    # Obtener información del sistema
    latency = round(bot.latency * 1000)
    guild_count = len(bot.guilds)
    member_count = sum(guild.member_count for guild in bot.guilds)
    
    # Determinar estado y color
    if bot_control.suspended:
        status_text = "🟡 SUSPENDIDO"
        status_color = 0xf39c12
        status_desc = "El bot está suspendido y no responde a comandos."
    else:
        status_text = "🟢 EN LÍNEA"
        status_color = 0x2ecc71
        status_desc = "El bot está funcionando normalmente."
    
    embed = discord.Embed(
        title="🌼 Estado del Bot",
        description=status_desc,
        color=status_color
    )
    
    embed.add_field(
        name="📊 Estado",
        value=status_text,
        inline=True
    )
    
    embed.add_field(
        name="⏱️ Latencia",
        value=f"{latency}ms",
        inline=True
    )
    
    embed.add_field(
        name="🌐 Servidores",
        value=str(guild_count),
        inline=True
    )
    
    embed.add_field(
        name="👥 Usuarios",
        value=str(member_count),
        inline=True
    )
    
    embed.add_field(
        name="🎵 Música",
        value=f"Colas activas: {len(music_system.queues)}",
        inline=True
    )
    
    # Estadísticas económicas si el sistema existe
    try:
        if 'economy_system' in globals():
            econ_stats = await economy_system.get_database_stats()
            embed.add_field(
                name="💰 Economía",
                value=f"Usuarios: {econ_stats['total_usuarios']}",
                inline=True
            )
    except:
        pass
    
    embed.set_footer(text=f"Solicitado por {ctx.author.display_name}")
    
    await ctx.send(embed=embed)

# ============ CONFIGURACIÓN INICIAL ============
@bot.event
async def on_ready():
    """Evento on_ready con información de control"""
    print(f'✅ {bot.user} conectado exitosamente!')
    print('🌼 Sistema de control cargado:')
    print('   !y on     - Activar bot')
    print('   !y off    - Suspender bot') 
    print('   !y 529244 - Apagar bot')
    print('   !status   - Ver estado del bot')
    
    # Configurar el owner del bot si no está establecido
    if bot.owner_id is None:
        try:
            app_info = await bot.application_info()
            bot.owner_id = app_info.owner.id
            print(f'👑 Owner del bot: {app_info.owner.name} ({bot.owner_id})')
        except Exception as e:
            print(f'⚠️ No se pudo obtener información del owner: {e}')
    
    try:
        synced = await bot.tree.sync()
        print(f'✅ {len(synced)} comandos sincronizados')
    except Exception as e:
        print(f'❌ Error sincronizando comandos: {e}')

























	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
# ============ SISTEMA PIXEL GIFT (JUEGO) ============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, 'caza_sombras', 'caza_sombras', 'backend')
SERVER_URL_FILE = os.path.join(BACKEND_DIR, 'public_url.txt')

def get_public_url():
    """Lee la URL pública desde el archivo"""
    try:
        if os.path.exists(SERVER_URL_FILE):
            with open(SERVER_URL_FILE, 'r') as f:
                url = f.read().strip()
                url = url.replace('\n', '').replace('\r', '')
                if url.startswith('https://'):
                    print(f"📄 URL leída: {url}")
                    return url
        print(f"❌ No se encontró URL válida en {SERVER_URL_FILE}")
        return None
    except Exception as e:
        print(f"❌ Error leyendo public_url.txt: {e}")
        return None

async def check_server_status(url):
    """Verifica si el servidor está activo"""
    try:
        print(f"🔍 Verificando servidor: {url}/health")
        response = requests.get(f"{url}/health", timeout=10)
        print(f"✅ Servidor responde: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ Servidor no responde: {e}")
        return False

async def check_game_accessible(url):
    """Verifica si el juego carga correctamente"""
    try:
        print(f"🎮 Verificando juego: {url}")
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

async def get_active_url():
    """Obtiene una URL activa SOLO mediante verificación"""
    public_url = get_public_url()
    
    if not public_url:
        print("❌ No se encontró URL pública")
        return None
    
    # Verificar si la URL está activa
    is_active = await check_server_status(public_url)
    is_game_accessible = await check_game_accessible(public_url)
    
    if is_active and is_game_accessible:
        print(f"✅ URL completamente operativa: {public_url}")
        return public_url
    elif is_active and not is_game_accessible:
        print(f"⚠️ URL responde pero juego no carga: {public_url}")
        return public_url  # Aún así retornamos la URL para intentar
    else:
        print(f"❌ URL no operable: {public_url}")
        return None

async def register_user_in_game(server_url, user_id, username):
    """Registra usuario en el juego"""
    try:
        print(f"👤 Registrando usuario: {username} ({user_id})")
        response = requests.post(
            f"{server_url}/api/register",
            json={
                "user_id": str(user_id),
                "username": username,
                "discord_name": username
            },
            timeout=10
        )
        success = response.status_code in [200, 409]
        print(f"📝 Registro {'exitoso' if success else 'fallido'}: {response.status_code}")
        return success
    except requests.exceptions.RequestException as e:
        print(f"❌ Error registrando usuario: {e}")
        return False

async def get_user_score_from_server(server_url, user_id):
    """Obtiene puntuación del usuario"""
    try:
        print(f"📊 Obteniendo score para usuario: {user_id}")
        response = requests.get(f"{server_url}/api/user/{user_id}", timeout=10)
        if response.status_code == 200:
            print(f"✅ Score obtenido para usuario: {user_id}")
            return response.json()
        else:
            print(f"❌ Usuario no encontrado o sin score: {user_id} - {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error obteniendo score: {e}")
        return None

async def get_top_scores_from_server(server_url, limit=10):
    """Obtiene ranking del servidor"""
    try:
        print(f"🏆 Obteniendo top {limit} scores")
        response = requests.get(f"{server_url}/api/leaderboard?limit={limit}", timeout=10)
        if response.status_code == 200:
            scores = response.json()
            print(f"✅ Ranking obtenido ({len(scores)} jugadores)")
            return scores
        else:
            print(f"❌ Error obteniendo ranking: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error obteniendo ranking: {e}")
        return None

def format_time(seconds):
    """Convierte segundos a formato mm:ss.ms"""
    if seconds >= 999999:  # Valor por defecto para "sin tiempo"
        return "No registrado"
    
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes:02d}:{secs:06.3f}"

@bot.tree.command(name="pixel_gift", description="Juega a Pixel Gift - ¡Menor tiempo gana!")
@app_commands.describe(
    action="Qué quieres hacer",
    user="Usuario para ver su tiempo"
)
@app_commands.choices(action=[
    app_commands.Choice(name="🎮 Jugar partida", value="play"),
    app_commands.Choice(name="⏱️ Ver mi tiempo", value="my_score"),
    app_commands.Choice(name="🏆 Ranking mejores tiempos", value="ranking"),
    app_commands.Choice(name="👤 Ver tiempo de usuario", value="user_score")
])
async def pixel_gift(interaction: discord.Interaction, 
                    action: app_commands.Choice[str] = None,
                    user: discord.User = None):
    
    action_value = action.value if action else "play"
    is_ephemeral = action_value != "ranking"
    
    print(f'🎮 Comando recibido: {action_value} por {interaction.user.name}')
    
    await interaction.response.defer(ephemeral=is_ephemeral)
    
    # OBTENER URL ACTIVA (SOLO VERIFICACIÓN, NO REINICIO)
    public_url = await get_active_url()
    
    if not public_url:
        error_msg = (
            "❌ **Servicio no disponible**\n\n"
            "El servidor del juego no está respondiendo. Esto puede deberse a:\n"
            "• El servicio de túnel no está activo\n"
            "• Hay problemas de conexión temporales\n\n"
            "**Solución:**\n"
            "3. Usa `/pixel_status` para ver el estado actual\n\n"
            "Si el problema persiste, contacta con un administrador.\n\n"
            "*Considerar que el sistema de **Cloudflare** seguramente ha fallado, esto se nota si la URL finaliza en `https://#####.cloudflare.com`*"
        )
        await interaction.followup.send(error_msg, ephemeral=True)
        return
    
    # VERIFICACIÓN ADICIONAL
    try:
        test_response = requests.get(f"{public_url}/health", timeout=5)
        if test_response.status_code != 200:
            raise Exception(f"Health check falló: {test_response.status_code}")
        print("✅ URL verificada y lista para usar")
    except Exception as e:
        error_msg = (
            f"❌ **Error de conexión**\n\n"
            f"La URL `{public_url}` no está respondiendo correctamente.\n\n"
            "**Por favor verifica:**\n"
            "• Que app.py esté ejecutándose correctamente\n"
            "• Que get_url.py esté activo y mostrando una URL válida\n"
            "• Usa `/pixel_status` para diagnóstico\n"
        )
        await interaction.followup.send(error_msg, ephemeral=True)
        return
    
    # PROCESAR COMANDOS
    if action_value == "play":
        # Registrar usuario automáticamente
        registration_success = await register_user_in_game(
            public_url, 
            interaction.user.id,
            f"{interaction.user.name}#{interaction.user.discriminator}"
        )
        
        game_url = f"{public_url}?id={interaction.user.id}"
        
        # Verificar accesibilidad del juego
        game_accessible = await check_game_accessible(public_url)
        
        embed = discord.Embed(
            title="🎮 Pixel Gift - Jugar",
            description=f"{interaction.user.mention} ¡Compite por el mejor tiempo!",
            color=0x00ff88 if game_accessible else 0xffa500
        )
        
        embed.add_field(
            name="🔗 Enlace de juego",
            value=f"[Jugar ahora]({game_url})",
            inline=False
        )
        
        embed.add_field(
            name="🏆 Objetivo",
            value="• **Menor tiempo = Mejor posición**\n• Recoge todos los regalos rápido\n• ¡Compite por el primer lugar!",
            inline=False
        )
        
        if not registration_success:
            embed.add_field(
                name="ℹ️ Registro",
                value="Tu usuario se registrará automáticamente al iniciar el juego",
                inline=False
            )
        
        if not game_accessible:
            embed.add_field(
                name="⚠️ Nota",
                value="El juego podría estar iniciando. Si no carga, espera unos segundos y vuelve a intentar.",
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        print(f"✅ Enlace de juego enviado a {interaction.user.name}")
    
    elif action_value == "my_score":
        user_data = await get_user_score_from_server(public_url, interaction.user.id)
        
        if user_data and user_data.get('score', 999999) < 999999:
            time_str = format_time(user_data['score'])
            embed = discord.Embed(
                title=f"⏱️ Mejor Tiempo de {interaction.user.mention}",
                color=0xffb347
            )
            embed.add_field(
                name="Tiempo",
                value=f"**{time_str}**",
                inline=False
            )
            
            # Obtener ranking para mostrar posición
            top_scores = await get_top_scores_from_server(public_url, 100)
            if top_scores:
                user_rank = next((i+1 for i, p in enumerate(top_scores) 
                               if p.get('user_id') == str(interaction.user.id)), None)
                if user_rank:
                    embed.add_field(
                        name="🏅 Posición en Ranking",
                        value=f"**#{user_rank}**",
                        inline=True
                    )
            
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(
                f"⏳ {interaction.user.mention} no tienes un tiempo registrado\n¡Juega con `/pixel_gift` para establecer tu primer tiempo!",
                ephemeral=True
            )
    
    elif action_value == "ranking":
        top_scores = await get_top_scores_from_server(public_url, 10)
        
        if not top_scores:
            await interaction.followup.send(
                "❌ No se pudieron cargar los tiempos del ranking\nEl servidor puede estar ocupado, intenta nuevamente.",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="🏆 Ranking - Mejores Tiempos",
            description="**Menor tiempo = Mejor posición**",
            color=0xffd700
        )
        
        ranking_text = ""
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, player in enumerate(top_scores[:10]):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            user_id = player.get('user_id')
            score = player.get('score', 999999)
            discord_name = player.get('discord_name', f'Usuario{user_id}')
            
            # Intentar obtener mención real
            try:
                discord_user = await bot.fetch_user(int(user_id))
                display_name = f"{discord_user.mention} ({discord_user.name})"
            except:
                display_name = discord_name
            
            time_str = format_time(score)
            ranking_text += f"{medal} {display_name} - `{time_str}`\n"
        
        embed.add_field(
            name="Top 10 Jugadores",
            value=ranking_text or "No hay tiempos registrados",
            inline=False
        )
        
        # Mostrar posición del usuario actual
        current_user_data = await get_user_score_from_server(public_url, interaction.user.id)
        if current_user_data and current_user_data.get('score', 999999) < 999999:
            user_rank = next((i+1 for i, p in enumerate(top_scores) 
                           if p.get('user_id') == str(interaction.user.id)), None)
            if user_rank:
                embed.add_field(
                    name="Tu Posición",
                    value=f"{interaction.user.mention} estás en **puesto #{user_rank}**",
                    inline=False
                )
        
        embed.set_footer(text="¡Usa /pixel_gift play para mejorar tu tiempo!")
        await interaction.followup.send(embed=embed, ephemeral=False)
    
    elif action_value == "user_score":
        if not user:
            await interaction.followup.send("❌ Debes mencionar un usuario", ephemeral=True)
            return
        
        user_data = await get_user_score_from_server(public_url, user.id)
        
        if user_data and user_data.get('score', 999999) < 999999:
            time_str = format_time(user_data['score'])
            embed = discord.Embed(
                title=f"⏱️ Mejor Tiempo de {user.mention}",
                color=0x00e0ff
            )
            embed.add_field(
                name="Tiempo",
                value=f"**{time_str}**",
                inline=False
            )
            embed.set_thumbnail(url=user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(
                f"⏳ {user.mention} no tiene un tiempo registrado",
                ephemeral=True
            )

@bot.tree.command(name="pixel_status", description="Verificar estado del servidor")
async def pixel_status(interaction: discord.Interaction):
    """Comando para verificar el estado actual del servidor"""
    await interaction.response.defer(ephemeral=True)
    
    public_url = get_public_url()
    
    embed = discord.Embed(title="🔍 Estado del Servidor Pixel Gift")
    
    if not public_url:
        embed.description = "❌ **URL NO CONFIGURADA**"
        embed.color = 0xff3333
        embed.add_field(
            name="Problema",
            value="No se encontró `public_url.txt` o está vacío",
            inline=False
        )
        embed.add_field(
            name="Solución", 
            value="Ejecuta `get_url.py` para generar la URL pública",
            inline=False
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    # Verificar estado del servidor
    try:
        health_response = requests.get(f"{public_url}/health", timeout=5)
        health_status = health_response.status_code == 200
        ping_time = health_response.elapsed.total_seconds() * 1000
    except:
        health_status = False
        ping_time = "N/A"
    
    # Verificar si el juego carga
    try:
        game_response = requests.get(public_url, timeout=5)
        game_status = game_response.status_code == 200
    except:
        game_status = False
    
    if health_status and game_status:
        embed.description = "🟢 **SERVICIO OPERATIVO**"
        embed.color = 0x00ff88
    elif health_status and not game_status:
        embed.description = "🟡 **SERVICIO PARCIAL**"
        embed.color = 0xffa500
    else:
        embed.description = "🔴 **SERVICIO NO DISPONIBLE**"
        embed.color = 0xff3333
    
    embed.add_field(name="🌐 URL Pública", value=f"`{public_url}`", inline=False)
    embed.add_field(name="📊 API Health", value="✅ Respondiendo" if health_status else "❌ No responde", inline=True)
    embed.add_field(name="🎮 Juego", value="✅ Cargando" if game_status else "❌ No carga", inline=True)
    
    if health_status:
        embed.add_field(name="⏱️ Ping", value=f"`{ping_time:.0f}ms`", inline=True)
    
    # Recomendaciones
    if not health_status:
        embed.add_field(
            name=">>> Recomendaciones",
            value="• Verifica que `app.py` esté ejecutándose\n>>> Ejecuta `get_url.py` si es necesario\n>>> • *estas acciones solo se pueden realizar en la terminal*",
            inline=False
        )
    elif not game_status:
        embed.add_field(
            name="🔧 Recomendaciones", 
            value="• El servidor está respondiendo pero el juego no carga\n• Espera unos segundos y reintenta\n• Verifica los templates",
            inline=False
        )
    else:
        embed.add_field(
            name="✅ Estado",
            value="¡Todo funciona correctamente! Puedes usar `/pixel_gift` para jugar.",
            inline=False
        )
    
    await interaction.followup.send(embed=embed, ephemeral=True)
	
	
	
	
	
	
	
try:
	bot.run(TOKEN)
except Exception as e:
	print(f"❌ Error crítico: {e}")
