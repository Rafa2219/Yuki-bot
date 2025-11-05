# Imports optimizados
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
from discord.ui import View, Button
import logging
import requests
import uuid
from datetime import datetime


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

# Configuración optimizada del bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot con configuración optimizada
bot = commands.Bot(
	command_prefix='!', 
	intents=intents, 
	help_command=None,
	max_messages=1000  # Reducir cache de mensajes
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

# ============ SISTEMA DE NORMALIZACIÓN OPTIMIZADO ============
def normalizar_comando(texto: str) -> str:
	"""Función optimizada para normalización de comandos"""
	if not texto.startswith('!'):
		return texto
	
	texto = texto.lower().strip()
	texto = unicodedata.normalize("NFD", texto)
	texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
	
	# Preservar menciones y espacios importantes
	texto = texto.replace("<#", " <#").replace("! ", "!").replace(" !","!")
	return ' '.join(texto.split())

# ============ EVENTOS PRINCIPALES ============
@bot.event
async def on_ready():
	"""Evento on_ready optimizado"""
	print(f'✅ {bot.user} conectado exitosamente!')
	
	try:
		synced = await bot.tree.sync()
		print(f'✅ {len(synced)} comandos sincronizados')
	except Exception as e:
		print(f'❌ Error sincronizando comandos: {e}')

@bot.event
async def on_member_join(member):
	"""Bienvenida optimizada"""
	channel = member.guild.get_channel(CONFIG['welcome_channel'])
	if channel:
		mensajes = [
			f"¡Hola {member.mention}! 🌸 Bienvenido/a a **{member.guild.name}** 💖",
			f"¡Bienvenid@ {member.mention}! 🎮 Espero que disfrutes en **{member.guild.name}**",
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
	"""Interceptación de mensajes optimizada"""
	if message.author.bot:
		return
	
	# Solo procesar si es un comando
	if message.content.startswith('!'):
		message.content = normalizar_comando(message.content)
		await bot.process_commands(message)

# ============ COMANDOS DE TEXTO OPTIMIZADOS ============
@bot.command(name='ayuda')
async def ayuda(ctx):
	"""Comando de ayuda humorístico"""
	respuestas = [
		"Q te pasa we?",
		"¿Necesitas ayuda? ¡Usa `!comandos`! ",
		"No sé we, ¿por qué me preguntas a mí?"
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
		title="✅ Estado del Servidor",
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
			"¿Quieres besarte a ti mismo? ",
			"Primero un cafecito, ¿no? ☕" 
			"Eso es un poco raro... "
		]
		await ctx.send(random.choice(respuestas))
		return

	respuestas = [
		f"\\*besa a {usuario.mention}\\* y luego sigue con su vida tranquila...",
		f"\\*besa a {usuario.mention}\\* y se queda sonriendo... 😊",
		f"¡Wow!\\n\\*besa a {usuario.mention}\\* y desaparece misteriosamente 🎭",
		f"¡Momento épico!\\n\\*besa a {usuario.mention}\\* y continúa su aventura ⚔️",
		f"\\*besa a {usuario.mention}\\* ",
		f"¡Sorpresa!\\n\\*besa a {usuario.mention}\\* y todos... \\n se quedan en silencio xd ",
		f"\\*besa a {usuario.mention}\\* y sonríe tímidamente... ",
		f"En secreto\\n\\*besa a {usuario.mention}\\* y se escabulle sin que nadie lo note ",
		f"Con estilo \\n \\*besa a {usuario.mention}\\* y hace una reverencia 🎩",
		f"\\*besa a {usuario.mention}\\* y luego se aleja lentamente… 🌸"
	]
	
	await ctx.send(random.choice(respuestas))

@bot.command(name='info')
async def info(ctx):
	"""Información del bot optimizada"""
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
	"""Saludo optimizado"""
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
	"""Comando humorístico optimizado"""
	respuesta = random.choice([
		"no sé we. ¿por qué me preguntas a mi?",
		"¿Yo qué sé? Pregúntale a Google",
		"Mmm... mejor pregúntale a alguien más"
	])
	await ctx.send(f"{respuesta} <:mmm:1429328016307130378>")

# ============ SISTEMA DE MÚSICA OPTIMIZADO ============
# ============ SISTEMA DE MÚSICA CON OPCIONES PREDEFINIDAS ============

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
        """Reproducir siguiente canción optimizado - CORREGIDO"""
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
        """Versión segura de play_next con manejo de errores"""
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

# Instancia del sistema de música corregido
music_system = MusicSystem()

# ============ COMANDOS DE MÚSICA ACTUALIZADOS ============
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
    """Comando de música unificado - CORREGIDO"""
    
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
		"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvpnugFc8GUOp116MXRshYsaBFrRRm-9etvg&usqp=CAU",
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
			"**😊 INTERACCIÓN SOCIAL**\n"
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
				"**🎭 COMANDOS DE INTERACCIÓN**\n"
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

# ============ COMANDO GUIAME OPTIMIZADO ============
@bot.tree.command(
	name="guiame",
	description="Muestra lista de canales de texto disponibles"
)
async def guiame(interaction: discord.Interaction):
	"""Comando guiame optimizado"""
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

# ============ NUEVA FUNCIÓN: SISTEMA DE ESTADÍSTICAS ============
@bot.tree.command(name="estadisticas", description="Muestra estadísticas del servidor")
async def estadisticas(interaction: discord.Interaction):
	"""NUEVA FUNCIÓN: Estadísticas del servidor"""
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




# ============ COMANDO DE RECOMENDACIONES CON CHOICES ============
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
            "• Opciones predefinidas con emojis\n"
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





# ============ SISTEMA DE ECONOMÍA Y GACHA ============
# Configuración de la economía (agregar al inicio del código)
ECONOMY_CONFIG = {
    'daily_coins': 100,
    'gacha_cost': 50,
    'starting_coins': 200,
    'max_inventory_size': 100
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
GACHA_ITEMS = {
    "personajes": [
        {"id": "char_001", "nombre": "Aventurero Novato", "tipo": "personaje", "rareza": "comun", "valor": 25},
        {"id": "char_002", "nombre": "Guerrero del Sol", "tipo": "personaje", "rareza": "raro", "valor": 75},
        {"id": "char_003", "nombre": "Mago Arcano", "tipo": "personaje", "rareza": "epico", "valor": 200},
        {"id": "char_004", "nombre": "Caballero Divino", "tipo": "personaje", "rareza": "legendario", "valor": 500},
        {"id": "char_005", "nombre": "Héroe del Destino", "tipo": "personaje", "rareza": "mitico", "valor": 1250}
    ],
    "armas": [
        {"id": "wep_001", "nombre": "Espada de Hierro", "tipo": "arma", "rareza": "comun", "valor": 20},
        {"id": "wep_002", "nombre": "Arco de Cazador", "tipo": "arma", "rareza": "comun", "valor": 20},
        {"id": "wep_003", "nombre": "Báculo Mágico", "tipo": "arma", "rareza": "raro", "valor": 60},
        {"id": "wep_004", "nombre": "Espada de Plata", "tipo": "arma", "rareza": "epico", "valor": 150},
        {"id": "wep_005", "nombre": "Hacha del Titán", "tipo": "arma", "rareza": "legendario", "valor": 400},
        {"id": "wep_006", "nombre": "Excalibur", "tipo": "arma", "rareza": "mitico", "valor": 1000}
    ],
    "artefactos": [
        {"id": "art_001", "nombre": "Anillo de Bronce", "tipo": "artefacto", "rareza": "comun", "valor": 15},
        {"id": "art_002", "nombre": "Amuleto de Fuerza", "tipo": "artefacto", "rareza": "raro", "valor": 45},
        {"id": "art_003", "nombre": "Capa de la Invisibilidad", "tipo": "artefacto", "rareza": "epico", "valor": 120},
        {"id": "art_004", "nombre": "Corona del Rey", "tipo": "artefacto", "rareza": "legendario", "valor": 300},
        {"id": "art_005", "nombre": "Orbe del Infinito", "tipo": "artefacto", "rareza": "mitico", "valor": 750}
    ],
    "mascotas": [
        {"id": "pet_001", "nombre": "Gatito", "tipo": "mascota", "rareza": "comun", "valor": 30},
        {"id": "pet_002", "nombre": "Lobo Joven", "tipo": "mascota", "rareza": "raro", "valor": 90},
        {"id": "pet_003", "nombre": "Fénix", "tipo": "mascota", "rareza": "epico", "valor": 250},
        {"id": "pet_004", "nombre": "Dragón", "tipo": "mascota", "rareza": "legendario", "valor": 600},
        {"id": "pet_005", "nombre": "Fénix Ancestral", "tipo": "mascota", "rareza": "mitico", "valor": 1500}
    ]
}

class EconomySystem:
    """Sistema de economía optimizado para alto tráfico - CORREGIDO"""
    
    def __init__(self):
        self.data_file = 'economy_data.json'
        self._cache = {}  # Cache en memoria para rápido acceso
        self._lock = asyncio.Lock()  # Lock para evitar condiciones de carrera
        self._load_data()
    
    def _load_data(self):
        """Cargar datos desde JSON - optimizado"""
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
        """Guardar datos a JSON - optimizado con backup"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando datos económicos: {e}")
    
    async def _atomic_operation(self, operation):
        """Ejecutar operación atómicamente con lock - CORREGIDO"""
        async with self._lock:
            try:
                result = await operation()  # CORREGIDO: añadir await
                # Guardar de forma asíncrona sin bloquear
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
        
        return "comun"  # Fallback
    
    def get_random_item(self, rarity: str):
        """Obtener item aleatorio de una rareza específica"""
        # Filtrar todos los items de la rareza deseada
        available_items = []
        for category in GACHA_ITEMS.values():
            for item in category:
                if item["rareza"] == rarity:
                    available_items.append(item)
        
        if available_items:
            item = random.choice(available_items).copy()
            # Añadir ID único y timestamp
            item["unique_id"] = str(uuid.uuid4())[:8]
            item["obtenido_en"] = datetime.now().isoformat()
            return item
        else:
            # Fallback: crear item genérico
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
        """Realizar un pull del gacha - CORREGIDO"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            # Verificar si tiene monedas
            if user_data["monedas"] < ECONOMY_CONFIG['gacha_cost']:
                return None, "❌ No tienes suficientes monedas"
            
            # Verificar espacio en inventario
            if len(user_data["inventario"]) >= ECONOMY_CONFIG['max_inventory_size']:
                return None, "❌ Tu inventario está lleno"
            
            # Realizar pull
            rarity = self.get_rarity()
            item = self.get_random_item(rarity)
            
            # Añadir a inventario
            user_data["inventario"].append(item)
            user_data["monedas"] -= ECONOMY_CONFIG['gacha_cost']
            user_data["total_gachas"] += 1
            
            # Si es personaje, añadir a lista de obtenidos
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
            
            # Buscar item en inventario del remitente
            item_index = None
            item_to_transfer = None
            
            for i, item in enumerate(from_user["inventario"]):
                if item.get("unique_id") == item_unique_id:
                    item_index = i
                    item_to_transfer = item
                    break
            
            if item_index is None:
                return False, "❌ Item no encontrado en tu inventario"
            
            # Verificar espacio en inventario del destinatario
            if len(to_user["inventario"]) >= ECONOMY_CONFIG['max_inventory_size']:
                return False, "❌ El inventario del destinatario está lleno"
            
            # Transferir item
            from_user["inventario"].pop(item_index)
            to_user["inventario"].append(item_to_transfer)
            
            return True, "✅ Item transferido exitosamente"
        
        return await self._atomic_operation(operation)
    
    async def sell_item(self, user_id: str, item_unique_id: str):
        """Vender item por monedas"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            # Buscar item en inventario
            item_index = None
            item_to_sell = None
            
            for i, item in enumerate(user_data["inventario"]):
                if item.get("unique_id") == item_unique_id:
                    item_index = i
                    item_to_sell = item
                    break
            
            if item_index is None:
                return False, "❌ Item no encontrado en tu inventario"
            
            # Calcular valor de venta (70% del valor original)
            sell_value = int(item_to_sell["valor"] * 0.7)
            
            # Vender item
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
            
            # Dar recompensa
            user_data = self.get_user_data(user_id)
            user_data["monedas"] += ECONOMY_CONFIG['daily_coins']
            self._cache["last_daily"][user_id_str] = today
            
            return True, f"✅ Recompensa diaria de {ECONOMY_CONFIG['daily_coins']} monedas obtenida"
        
        return await self._atomic_operation(operation)

# Instancia global del sistema económico
economy_system = EconomySystem()

import asyncio
import discord
from discord.ext import commands
from discord.ui import View, Button
import json
import os
import random
import uuid
from datetime import datetime
import logging

# Configuración de logging
logger = logging.getLogger('discord_bot')

# ============ SISTEMA DE ECONOMÍA Y GACHA ============
# Configuración de la economía (agregar al inicio del código)
ECONOMY_CONFIG = {
    'daily_coins': 100,
    'gacha_cost': 50,
    'starting_coins': 200,
    'max_inventory_size': 100
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
GACHA_ITEMS = {
    "personajes": [
        {"id": "char_001", "nombre": "Aventurero Novato", "tipo": "personaje", "rareza": "comun", "valor": 25},
        {"id": "char_002", "nombre": "Guerrero del Sol", "tipo": "personaje", "rareza": "raro", "valor": 75},
        {"id": "char_003", "nombre": "Mago Arcano", "tipo": "personaje", "rareza": "epico", "valor": 200},
        {"id": "char_004", "nombre": "Caballero Divino", "tipo": "personaje", "rareza": "legendario", "valor": 500},
        {"id": "char_005", "nombre": "Héroe del Destino", "tipo": "personaje", "rareza": "mitico", "valor": 1250}
    ],
    "armas": [
        {"id": "wep_001", "nombre": "Espada de Hierro", "tipo": "arma", "rareza": "comun", "valor": 20},
        {"id": "wep_002", "nombre": "Arco de Cazador", "tipo": "arma", "rareza": "comun", "valor": 20},
        {"id": "wep_003", "nombre": "Báculo Mágico", "tipo": "arma", "rareza": "raro", "valor": 60},
        {"id": "wep_004", "nombre": "Espada de Plata", "tipo": "arma", "rareza": "epico", "valor": 150},
        {"id": "wep_005", "nombre": "Hacha del Titán", "tipo": "arma", "rareza": "legendario", "valor": 400},
        {"id": "wep_006", "nombre": "Excalibur", "tipo": "arma", "rareza": "mitico", "valor": 1000}
    ],
    "artefactos": [
        {"id": "art_001", "nombre": "Anillo de Bronce", "tipo": "artefacto", "rareza": "comun", "valor": 15},
        {"id": "art_002", "nombre": "Amuleto de Fuerza", "tipo": "artefacto", "rareza": "raro", "valor": 45},
        {"id": "art_003", "nombre": "Capa de la Invisibilidad", "tipo": "artefacto", "rareza": "epico", "valor": 120},
        {"id": "art_004", "nombre": "Corona del Rey", "tipo": "artefacto", "rareza": "legendario", "valor": 300},
        {"id": "art_005", "nombre": "Orbe del Infinito", "tipo": "artefacto", "rareza": "mitico", "valor": 750}
    ],
    "mascotas": [
        {"id": "pet_001", "nombre": "Gatito", "tipo": "mascota", "rareza": "comun", "valor": 30},
        {"id": "pet_002", "nombre": "Lobo Joven", "tipo": "mascota", "rareza": "raro", "valor": 90},
        {"id": "pet_003", "nombre": "Fénix", "tipo": "mascota", "rareza": "epico", "valor": 250},
        {"id": "pet_004", "nombre": "Dragón", "tipo": "mascota", "rareza": "legendario", "valor": 600},
        {"id": "pet_005", "nombre": "Fénix Ancestral", "tipo": "mascota", "rareza": "mitico", "valor": 1500}
    ]
}

class EconomySystem:
    """Sistema de economía optimizado para alto tráfico - CORREGIDO"""
    
    def __init__(self):
        self.data_file = 'economy_data.json'
        self._cache = {}  # Cache en memoria para rápido acceso
        self._lock = asyncio.Lock()  # Lock para evitar condiciones de carrera
        self._active_sales = {}  # Diccionario para rastrear ventas activas por usuario
        self._load_data()
    
    def _load_data(self):
        """Cargar datos desde JSON - optimizado"""
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
        """Guardar datos a JSON - optimizado con backup"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error guardando datos económicos: {e}")
    
    async def _atomic_operation(self, operation):
        """Ejecutar operación atómicamente con lock - CORREGIDO"""
        async with self._lock:
            try:
                result = await operation()  # CORREGIDO: añadir await
                # Guardar de forma asíncrona sin bloquear
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
        
        return "comun"  # Fallback
    
    def get_random_item(self, rarity: str):
        """Obtener item aleatorio de una rareza específica"""
        # Filtrar todos los items de la rareza deseada
        available_items = []
        for category in GACHA_ITEMS.values():
            for item in category:
                if item["rareza"] == rarity:
                    available_items.append(item)
        
        if available_items:
            item = random.choice(available_items).copy()
            # Añadir ID único y timestamp
            item["unique_id"] = str(uuid.uuid4())[:8]
            item["obtenido_en"] = datetime.now().isoformat()
            return item
        else:
            # Fallback: crear item genérico
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
        """Realizar un pull del gacha - CORREGIDO"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            # Verificar si tiene monedas
            if user_data["monedas"] < ECONOMY_CONFIG['gacha_cost']:
                return None, "❌ No tienes suficientes monedas"
            
            # Verificar espacio en inventario
            if len(user_data["inventario"]) >= ECONOMY_CONFIG['max_inventory_size']:
                return None, "❌ Tu inventario está lleno"
            
            # Realizar pull
            rarity = self.get_rarity()
            item = self.get_random_item(rarity)
            
            # Añadir a inventario
            user_data["inventario"].append(item)
            user_data["monedas"] -= ECONOMY_CONFIG['gacha_cost']
            user_data["total_gachas"] += 1
            
            # Si es personaje, añadir a lista de obtenidos
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
            
            # Buscar item en inventario del remitente
            item_index = None
            item_to_transfer = None
            
            for i, item in enumerate(from_user["inventario"]):
                if item.get("unique_id") == item_unique_id:
                    item_index = i
                    item_to_transfer = item
                    break
            
            if item_index is None:
                return False, "❌ Item no encontrado en tu inventario"
            
            # Verificar espacio en inventario del destinatario
            if len(to_user["inventario"]) >= ECONOMY_CONFIG['max_inventory_size']:
                return False, "❌ El inventario del destinatario está lleno"
            
            # Transferir item
            from_user["inventario"].pop(item_index)
            to_user["inventario"].append(item_to_transfer)
            
            return True, "✅ Item transferido exitosamente"
        
        return await self._atomic_operation(operation)
    
    async def sell_item(self, user_id: str, item_unique_id: str):
        """Vender item por monedas"""
        async def operation():
            user_data = self.get_user_data(user_id)
            
            # Buscar item en inventario
            item_index = None
            item_to_sell = None
            
            for i, item in enumerate(user_data["inventario"]):
                if item.get("unique_id") == item_unique_id:
                    item_index = i
                    item_to_sell = item
                    break
            
            if item_index is None:
                return False, "❌ Item no encontrado en tu inventario"
            
            # Calcular valor de venta (70% del valor original)
            sell_value = int(item_to_sell["valor"] * 0.7)
            
            # Vender item
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
            
            # Dar recompensa
            user_data = self.get_user_data(user_id)
            user_data["monedas"] += ECONOMY_CONFIG['daily_coins']
            self._cache["last_daily"][user_id_str] = today
            
            return True, f"✅ Recompensa diaria de {ECONOMY_CONFIG['daily_coins']} monedas obtenida"
        
        return await self._atomic_operation(operation)
    
    async def transfer_coins(self, from_user_id: str, to_user_id: str, amount: int):
        """Transferir monedas entre usuarios"""
        async def operation():
            from_user = self.get_user_data(from_user_id)
            to_user = self.get_user_data(to_user_id)
            
            if from_user["monedas"] < amount:
                return False, "❌ No tienes suficientes monedas"
            
            if amount <= 0:
                return False, "❌ La cantidad debe ser mayor a 0"
            
            # Transferir monedas
            from_user["monedas"] -= amount
            to_user["monedas"] += amount
            
            return True, f"✅ {amount} monedas transferidas exitosamente"
        
        return await self._atomic_operation(operation)

# Instancia global del sistema económico
economy_system = EconomySystem()

# ============ COMANDOS DE ECONOMÍA MEJORADOS ============

# Diccionario para rastrear ventas activas y evitar conflictos
active_sales = {}

@bot.command(name='gacha')
async def gacha(ctx):
    """Comando para usar el sistema gacha - CORREGIDO"""
    try:
        # Mostrar embed de confirmación
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
        cancel_button = Button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
        
        async def confirm_callback(interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("❌ Este menú no es para ti", ephemeral=True)
                return
            
            # CORREGIDO: Usar interaction.user.id en lugar de ctx.author.id
            result = await economy_system.gacha_pull(str(interaction.user.id))
            
            if result is None:
                await interaction.response.send_message("❌ Error en el sistema gacha", ephemeral=True)
                return
            
            item, message = result  # CORREGIDO: Desempaquetar el resultado
            
            if item is None:
                await interaction.response.send_message(message, ephemeral=True)
                return
            
            # Crear embed del resultado
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
            
            # Añadir emoji según rareza
            rarity_emojis = {
                "comun": "⚪",
                "raro": "🔵", 
                "epico": "🟣",
                "legendario": "🟠",
                "mitico": "🟡"
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
        cancel_button.callback = cancel_callback
        
        view.add_item(confirm_button)
        view.add_item(cancel_button)
        
        await ctx.send(embed=embed, view=view)
        
    except Exception as e:
        logger.error(f"Error en comando gacha: {e}")
        await ctx.send("❌ Error al usar el gacha")

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
        
        # Crear embed del inventario
        embed = discord.Embed(
            title=f"🎒 Inventario de {ctx.author.mention}",
            description=f"**Monedas:** {user_data['monedas']} | **Total items:** {total_items}",
            color=0x3498db
        )
        
        # Añadir items a la página actual
        for i, item in enumerate(items, start=(pagina-1)*10 + 1):
            emoji = {"comun": "🪨"  , "raro": "💠", "epico": "💎", "legendario": "⚜️", "mitico": "🏆"}.get(item["rareza"], "⚪")
            embed.add_field(
                name=f"{emoji} {item['nombre']}",
                value=(
                    f"**Rareza:** {item['rareza'].title()}\n"
                    f"**Valor:** {item['valor']} monedas\n"
                    f"**ID:** `{item['unique_id']}`"
                ),
                inline=True
            )
        
        embed.set_footer(text=f"Página {pagina}/{total_pages} | Usa !inventario <número> para navegar")
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        logger.error(f"Error en comando inventario: {e}")
        await ctx.send("❌ Error al ver el inventario")


#Transferir
@bot.command(name='transferir')
async def transferir(ctx, usuario: discord.Member = None, item_id: str = None):
    """Transferir item a otro usuario"""
    try:
        # Verificar parámetros básicos
        if usuario is None or item_id is None:
            embed = discord.Embed(
                title="❌ Uso incorrecto",
                description="Usa: `!transferir @usuario <item_id>`\n\nEjemplo: `!transferir @amigo abc123`",
                color=0xe74c3c
            )
            await ctx.send(embed=embed)
            return

        # Verificaciones básicas
        if usuario.id == ctx.author.id:
            embed = discord.Embed(
                title="❌ Transferencia inválida",
                description="No puedes transferir items a ti mismo",
                color=0xe74c3c
            )
            await ctx.send(embed=embed)
            return

        if usuario.bot:
            embed = discord.Embed(
                title="❌ Transferencia inválida",
                description="No puedes transferir items a bots",
                color=0xe74c3c
            )
            await ctx.send(embed=embed)
            return

        # Obtener datos del usuario
        user_data = economy_system.get_user_data(str(ctx.author.id))
        target_user_data = economy_system.get_user_data(str(usuario.id))

        # Buscar item en inventario
        item_encontrado = None
        for item in user_data["inventario"]:
            if item.get("unique_id") == item_id:
                item_encontrado = item
                break

        if not item_encontrado:
            embed = discord.Embed(
                title="❌ Item no encontrado",
                description=f"No tienes ningún item con el ID `{item_id}` en tu inventario",
                color=0xe74c3c
            )
            embed.add_field(
                name="💡 Consejo",
                value="Usa `!inventario` para ver tus items y sus IDs",
                inline=False
            )
            await ctx.send(embed=embed)
            return

        # Verificar espacio en inventario del destinatario
        if len(target_user_data["inventario"]) >= ECONOMY_CONFIG['max_inventory_size']:
            embed = discord.Embed(
                title="❌ Inventario lleno",
                description=f"El inventario de {usuario.mention} está lleno\nNo puede recibir más items",
                color=0xe74c3c
            )
            embed.add_field(
                name="Límite actual",
                value=f"{ECONOMY_CONFIG['max_inventory_size']} items",
                inline=True
            )
            await ctx.send(embed=embed)
            return

        # Crear embed de confirmación
        rarity_color = RARITY_SYSTEM[item_encontrado["rareza"]]["color"]
        embed = discord.Embed(
            title="🔄 Confirmar Transferencia",
            description=f"¿Estás seguro de que quieres transferir este item a {usuario.mention}?",
            color=rarity_color
        )
        
        embed.add_field(
            name="📦 Item a transferir",
            value=(
                f"**Nombre:** {item_encontrado['nombre']}\n"
                f"**Tipo:** {item_encontrado['tipo'].title()}\n"
                f"**Rareza:** {item_encontrado['rareza'].title()}\n"
                f"**Valor:** {item_encontrado['valor']} monedas\n"
                f"**ID:** `{item_encontrado['unique_id']}`"
            ),
            inline=False
        )
        
        embed.add_field(
            name="👤 Destinatario",
            value=f"{usuario.mention} ({usuario.display_name})",
            inline=True
        )
        
        embed.add_field(
            name="📊 Inventarios",
            value=(
                f"**Tu inventario:** {len(user_data['inventario'])}/{ECONOMY_CONFIG['max_inventory_size']} items\n"
                f"**Inventario destino:** {len(target_user_data['inventario'])}/{ECONOMY_CONFIG['max_inventory_size']} items"
            ),
            inline=True
        )
        
        embed.set_footer(text="Esta acción no se puede deshacer")

        # Crear vista con botones de confirmación
        view = View(timeout=30)
        
        async def confirm_callback(interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("❌ Esta confirmación no es para ti", ephemeral=True)
                return
            
            # Realizar la transferencia
            result = await economy_system.transfer_item(str(ctx.author.id), str(usuario.id), item_id)
            
            if result is None:
                await interaction.response.edit_message(
                    embed=discord.Embed(
                        title="❌ Error en el sistema",
                        description="Ocurrió un error al procesar la transferencia",
                        color=0xe74c3c
                    ),
                    view=None
                )
                return
            
            success, message = result
            
            if success:
                # Obtener datos actualizados
                user_updated = economy_system.get_user_data(str(ctx.author.id))
                target_updated = economy_system.get_user_data(str(usuario.id))
                
                embed_success = discord.Embed(
                    title="✅ Transferencia Completada",
                    description=f"Has transferido exitosamente un item a {usuario.mention}",
                    color=0x2ecc71
                )
                
                embed_success.add_field(
                    name="📦 Item transferido",
                    value=(
                        f"**{item_encontrado['nombre']}**\n"
                        f"*{item_encontrado['tipo'].title()} • {item_encontrado['rareza'].title()}*"
                    ),
                    inline=False
                )
                
                embed_success.add_field(
                    name="📊 Inventarios actualizados",
                    value=(
                        f"**{ctx.author.display_name}:** {len(user_updated['inventario'])} items\n"
                        f"**{usuario.display_name}:** {len(target_updated['inventario'])} items"
                    ),
                    inline=True
                )
                
                embed_success.add_field(
                    name="🆔 ID del item",
                    value=f"`{item_encontrado['unique_id']}`",
                    inline=True
                )
                
                # Notificar al destinatario si está en el servidor
                try:
                    notify_embed = discord.Embed(
                        title="🎁 ¡Has recibido un item!",
                        description=f"{ctx.author.mention} te ha transferido un item",
                        color=rarity_color
                    )
                    notify_embed.add_field(
                        name="📦 Item recibido",
                        value=(
                            f"**Nombre:** {item_encontrado['nombre']}\n"
                            f"**Tipo:** {item_encontrado['tipo'].title()}\n"
                            f"**Rareza:** {item_encontrado['rareza'].title()}\n"
                            f"**Valor:** {item_encontrado['valor']} monedas"
                        ),
                        inline=False
                    )
                    notify_embed.set_footer(text=f"ID: {item_encontrado['unique_id']}")
                    
                    await usuario.send(embed=notify_embed)
                except:
                    pass  # No se pudo enviar DM, pero la transferencia fue exitosa
                
                await interaction.response.edit_message(embed=embed_success, view=None)
                
            else:
                embed_error = discord.Embed(
                    title="❌ Error en la transferencia",
                    description=message,
                    color=0xe74c3c
                )
                await interaction.response.edit_message(embed=embed_error, view=None)
        
        async def cancel_callback(interaction):
            if interaction.user.id != ctx.author.id:
                await interaction.response.send_message("❌ Esta confirmación no es para ti", ephemeral=True)
                return
            
            embed_cancel = discord.Embed(
                title="❌ Transferencia Cancelada",
                description="La transferencia ha sido cancelada",
                color=0x95a5a6
            )
            await interaction.response.edit_message(embed=embed_cancel, view=None)
        
        async def timeout_callback():
            try:
                embed_timeout = discord.Embed(
                    title="⏰ Tiempo agotado",
                    description="La confirmación de transferencia ha expirado",
                    color=0x95a5a6
                )
                # Intentar editar el mensaje original
                message = await ctx.channel.fetch_message(view.message.id)
                await message.edit(embed=embed_timeout, view=None)
            except:
                pass
        
        confirm_button = Button(label="✅ Confirmar", style=discord.ButtonStyle.success)
        cancel_button = Button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
        
        confirm_button.callback = confirm_callback
        cancel_button.callback = cancel_callback
        
        view.add_item(confirm_button)
        view.add_item(cancel_button)
        view.on_timeout = timeout_callback
        
        message = await ctx.send(embed=embed, view=view)
        view.message = message
        
    except Exception as e:
        logger.error(f"Error en comando transferir: {e}")
        embed_error = discord.Embed(
            title="❌ Error en el sistema",
            description="Ocurrió un error al procesar el comando de transferencia",
            color=0xe74c3c
        )
        embed_error.add_field(
            name="Uso correcto",
            value="`!transferir @usuario <item_id>`",
            inline=False
        )
        await ctx.send(embed=embed_error)
        

#pay
@bot.command(name='pay')
async def pay(ctx, usuario: discord.Member, cantidad: int):
    """Transferir monedas a otro usuario"""
    try:
        if usuario.id == ctx.author.id:
            await ctx.send("❌ No puedes transferir monedas a ti mismo")
            return
        
        if cantidad <= 0:
            await ctx.send("❌ La cantidad debe ser mayor a 0")
            return
        
        # Verificar que el remitente tiene suficiente dinero
        sender_data = economy_system.get_user_data(str(ctx.author.id))
        if sender_data["monedas"] < cantidad:
            await ctx.send(f"❌ No tienes suficientes monedas. Tienes {sender_data['monedas']} monedas")
            return
        
        # Transferir monedas
        result = await economy_system.transfer_coins(str(ctx.author.id), str(usuario.id), cantidad)
        
        if result is None:
            await ctx.send("❌ Error en el sistema de transferencia")
            return
        
        success, message = result
        
        if success:
            # Obtener datos actualizados
            sender_final = economy_system.get_user_data(str(ctx.author.id))
            receiver_final = economy_system.get_user_data(str(usuario.id))
            
            embed = discord.Embed(
                title="✅ Transferencia Exitosa",
                description=f"Has transferido {cantidad} monedas a {usuario.mention}",
                color=0x2ecc71
            )
            embed.add_field(
                name="💰 Saldos actualizados",
                value=(
                    f"**{ctx.author.display_name}:** {sender_final['monedas']} monedas (-{cantidad})\n"
                    f"**{usuario.display_name}:** {receiver_final['monedas']} monedas (+{cantidad})"
                ),
                inline=False
            )
            
            await ctx.send(embed=embed)
        else:
            await ctx.send(message)
            
    except Exception as e:
        logger.error(f"Error en comando pay: {e}")
        await ctx.send("❌ Error al transferir monedas")

#venta de artículos
@bot.command(name='vender')
async def vender(ctx, mencion: discord.Member = None, item_id: str = None, precio: int = None):
    """Vender item por monedas o a otro usuario"""
    try:
        # Verificar parámetros básicos
        if item_id is None:
            await ctx.send("❌ Debes especificar el ID del item. Usa: `!vender [@usuario] <item_id> [precio]`")
            return

        # Verificar si el usuario ya tiene una venta activa
        if str(ctx.author.id) in active_sales:
            await ctx.send("❌ Ya tienes una venta activa. Espera a que termine antes de crear otra.")
            return

        user_data = economy_system.get_user_data(str(ctx.author.id))
        
        # Buscar item en inventario
        item_encontrado = None
        for item in user_data["inventario"]:
            if item.get("unique_id") == item_id:
                item_encontrado = item
                break

        if not item_encontrado:
            await ctx.send("❌ Item no encontrado en tu inventario")
            return

        valor_real = item_encontrado["valor"]
        
        # Caso 1: Venta al bot (sin mención o mención al bot)
        if mencion is None or mencion.id == bot.user.id:
            if precio is not None:
                await ctx.send("⚠️ El bot siempre compra los items al 70% de su valor. El precio especificado será ignorado.")
            
            valor_venta = int(valor_real * 0.7)
            result = await economy_system.sell_item(str(ctx.author.id), item_id)
            
            if result is None:
                await ctx.send("❌ Error en el sistema de venta")
                return
            
            success, message = result
            
            if success:
                embed = discord.Embed(
                    title="🌼 Venta al Sistema",
                    description=(
                        f"**Item:** {item_encontrado['nombre']}\n"
                        f"**Valor original:** {valor_real} monedas\n"
                        f"**Valor de venta (70%):** {valor_venta} monedas\n\n"
                        f"{message}\n"
                        f"**Monedas actuales:** {user_data['monedas']}"
                    ),
                    color=0xf39c12
                )
                embed.set_footer(text="El sistema compra automáticamente al 70% del valor")
                await ctx.send(embed=embed)
            else:
                await ctx.send(message)

        # Caso 2: Venta a otro usuario específico
        elif mencion.id != ctx.author.id and mencion.id != bot.user.id:
            # Verificar que el usuario objetivo existe
            target_user_data = economy_system.get_user_data(str(mencion.id))
            
            # Si no se especifica precio, usar valor real
            if precio is None:
                precio = valor_real
                porcentaje = "100%"
            else:
                # Calcular porcentaje del valor real
                if valor_real > 0:
                    porcentaje_valor = (precio / valor_real) * 100
                    porcentaje = f"{porcentaje_valor:.1f}%"
                else:
                    porcentaje = "N/A"

            # Crear embed de oferta de venta
            embed = discord.Embed(
                title="💰 Oferta de Venta",
                description=(
                    f"{ctx.author.mention} quiere vender un item a {mencion.mention}\n\n"
                    f"**Item:** {item_encontrado['nombre']}\n"
                    f"**Tipo:** {item_encontrado['tipo'].title()}\n"
                    f"**Rareza:** {item_encontrado['rareza'].title()}\n"
                    f"**Valor de referencia:** {valor_real} monedas\n"
                    f"**Precio de venta:** {precio} monedas\n"
                    f"**Esto es el:** {porcentaje} del valor real"
                ),
                color=RARITY_SYSTEM[item_encontrado["rareza"]]["color"]
            )
            
            # Configurar timeout fijo (sin contador visual)
            timeout_seconds = 60
            embed.set_footer(text=f"ID del item: {item_id} | La oferta expira en 60 segundos")

            # Crear botones para aceptar/rechazar
            view = View(timeout=timeout_seconds)
            
            # Registrar venta activa
            active_sales[str(ctx.author.id)] = {
                "item_id": item_id,
                "message_id": None,
                "buyer_id": str(mencion.id)
            }
            
            async def accept_callback(interaction):
                if interaction.user.id != mencion.id:
                    await interaction.response.send_message("❌ Esta oferta no es para ti", ephemeral=True)
                    return
                
                # Verificar que el comprador tiene suficiente dinero
                comprador_actual_data = economy_system.get_user_data(str(mencion.id))
                if comprador_actual_data["monedas"] < precio:
                    await interaction.response.send_message(
                        f"❌ No tienes suficientes monedas. Necesitas {precio} monedas pero tienes {comprador_actual_data['monedas']}",
                        ephemeral=True
                    )
                    # Limpiar venta activa
                    if str(ctx.author.id) in active_sales:
                        del active_sales[str(ctx.author.id)]
                    return
                
                # Verificar que el vendedor aún tiene el item
                vendedor_actual_data = economy_system.get_user_data(str(ctx.author.id))
                item_still_exists = any(item.get("unique_id") == item_id for item in vendedor_actual_data["inventario"])
                
                if not item_still_exists:
                    await interaction.response.send_message("❌ El vendedor ya no tiene este item", ephemeral=True)
                    # Limpiar venta activa
                    if str(ctx.author.id) in active_sales:
                        del active_sales[str(ctx.author.id)]
                    return
                
                # Realizar la transacción
                success_transfer, msg_transfer = await economy_system.transfer_item(
                    str(ctx.author.id), str(mencion.id), item_id
                )
                
                if success_transfer:
                    # Transferir el dinero
                    await economy_system.remove_coins(str(mencion.id), precio)
                    await economy_system.add_coins(str(ctx.author.id), precio)
                    
                    # Obtener datos actualizados
                    vendedor_final_data = economy_system.get_user_data(str(ctx.author.id))
                    comprador_final_data = economy_system.get_user_data(str(mencion.id))
                    
                    embed_success = discord.Embed(
                        title="✅ Venta Completada",
                        description=(
                            f"**Item:** {item_encontrado['nombre']}\n"
                            f"**Precio:** {precio} monedas\n"
                            f"**Comprador:** {mencion.mention}\n"
                            f"**Vendedor:** {ctx.author.mention}"
                        ),
                        color=0x2ecc71
                    )
                    embed_success.add_field(
                        name="💰 Saldos actualizados",
                        value=(
                            f"**{ctx.author.display_name}:** {vendedor_final_data['monedas']} monedas (+{precio})\n"
                            f"**{mencion.display_name}:** {comprador_final_data['monedas']} monedas (-{precio})"
                        ),
                        inline=False
                    )
                    
                    # Deshabilitar los botones y mantener el mensaje original
                    for item in view.children:
                        item.disabled = True
                    
                    await interaction.response.edit_message(embed=embed_success, view=view)
                else:
                    await interaction.response.send_message(f"❌ Error en la transacción: {msg_transfer}", ephemeral=True)
                
                # Limpiar venta activa
                if str(ctx.author.id) in active_sales:
                    del active_sales[str(ctx.author.id)]
            
            async def reject_callback(interaction):
                if interaction.user.id != mencion.id:
                    await interaction.response.send_message("❌ Esta oferta no es para ti", ephemeral=True)
                    return
                
                embed_rejected = discord.Embed(
                    title="❌ Venta Rechazada",
                    description=f"{mencion.mention} ha rechazado la oferta de compra",
                    color=0xe74c3c
                )
                
                # Deshabilitar los botones y mantener el mensaje original
                for item in view.children:
                    item.disabled = True
                
                await interaction.response.edit_message(embed=embed_rejected, view=view)
                
                # Limpiar venta activa
                if str(ctx.author.id) in active_sales:
                    del active_sales[str(ctx.author.id)]
            
            async def timeout_callback():
                """Callback cuando el tiempo se agota"""
                # Solo procesar el timeout si la venta sigue activa
                if str(ctx.author.id) not in active_sales:
                    return
                    
                try:
                    embed_expired = discord.Embed(
                        title="⏰ Oferta Expirada",
                        description="La oferta de venta ha expirado (60 segundos)",
                        color=0x95a5a6
                    )
                    
                    # Buscar el mensaje original
                    try:
                        message_obj = await ctx.channel.fetch_message(active_sales[str(ctx.author.id)]["message_id"])
                        await message_obj.edit(embed=embed_expired, view=None)
                    except:
                        pass  # Si no se puede encontrar el mensaje, ignorar
                        
                except Exception as e:
                    print(f"Error al editar mensaje expirado: {e}")
                
                # Limpiar venta activa
                if str(ctx.author.id) in active_sales:
                    del active_sales[str(ctx.author.id)]
            
            accept_button = Button(label="✅ Aceptar", style=discord.ButtonStyle.success)
            reject_button = Button(label="❌ Rechazar", style=discord.ButtonStyle.danger)
            
            accept_button.callback = accept_callback
            reject_button.callback = reject_callback
            
            view.add_item(accept_button)
            view.add_item(reject_button)
            view.on_timeout = timeout_callback
            
            message = await ctx.send(embed=embed, view=view)
            
            # Actualizar el ID del mensaje en la venta activa
            active_sales[str(ctx.author.id)]["message_id"] = message.id

        # Caso 3: Venta pública (usando una palabra clave especial)
        else:
            await ctx.send("❌ No puedes venderte items a ti mismo. Para venta pública usa: `!vender_publico <item_id> <precio>`")

    except Exception as e:
        logger.error(f"Error en comando vender: {e}")
        # Limpiar venta activa en caso de error
        if str(ctx.author.id) in active_sales:
            del active_sales[str(ctx.author.id)]
        await ctx.send("❌ Error al procesar la venta. Usa: `!vender [@usuario] <item_id> [precio]`")

# Nuevo comando para ventas públicas
@bot.command(name='vender_publico')
async def vender_publico(ctx, item_id: str = None, precio: int = None):
    """Vender un item públicamente a cualquier miembro del servidor"""
    try:
        # Verificar parámetros básicos
        if item_id is None:
            await ctx.send("❌ Debes especificar el ID del item. Usa: `!vender_publico <item_id> <precio>`")
            return

        # Verificar si el usuario ya tiene una venta activa
        if str(ctx.author.id) in active_sales:
            await ctx.send("❌ Ya tienes una venta activa. Espera a que termine antes de crear otra.")
            return

        user_data = economy_system.get_user_data(str(ctx.author.id))
        
        # Buscar item en inventario
        item_encontrado = None
        for item in user_data["inventario"]:
            if item.get("unique_id") == item_id:
                item_encontrado = item
                break

        if not item_encontrado:
            await ctx.send("❌ Item no encontrado en tu inventario")
            return

        valor_real = item_encontrado["valor"]
        
        # Si no se especifica precio, usar valor real
        if precio is None:
            precio = valor_real
            porcentaje = "100%"
        else:
            # Calcular porcentaje del valor real
            if valor_real > 0:
                porcentaje_valor = (precio / valor_real) * 100
                porcentaje = f"{porcentaje_valor:.1f}%"
            else:
                porcentaje = "N/A"

        embed = discord.Embed(
            title="🌍 Venta Pública",
            description=(
                f"{ctx.author.mention} está vendiendo un item públicamente\n\n"
                f"**Item:** {item_encontrado['nombre']}\n"
                f"**Tipo:** {item_encontrado['tipo'].title()}\n"
                f"**Rareza:** {item_encontrado['rareza'].title()}\n"
                f"**Valor de referencia:** {valor_real} monedas\n"
                f"**Precio de venta:** {precio} monedas\n"
                f"**Esto es el:** {porcentaje} del valor real"
            ),
            color=RARITY_SYSTEM[item_encontrado["rareza"]]["color"]
        )
        embed.set_footer(text=f"ID del item: {item_id} | Cualquier miembro puede comprar | Expira en 60 segundos")

        view = View(timeout=60)
        
        # Registrar venta activa
        active_sales[str(ctx.author.id)] = {
            "item_id": item_id,
            "message_id": None,
            "buyer_id": "public",
            "price": precio
        }
        
        async def public_buy_callback(interaction):
            buyer_id = str(interaction.user.id)
            
            # El vendedor no puede comprar su propio item
            if buyer_id == str(ctx.author.id):
                await interaction.response.send_message("❌ No puedes comprar tu propio item", ephemeral=True)
                return
            
            # Verificar que el comprador tiene suficiente dinero
            buyer_data = economy_system.get_user_data(buyer_id)
            if buyer_data["monedas"] < precio:
                await interaction.response.send_message(
                    f"❌ No tienes suficientes monedas. Necesitas {precio} monedas pero tienes {buyer_data['monedas']}",
                    ephemeral=True
                )
                return
            
            # Verificar que el vendedor aún tiene el item
            seller_data = economy_system.get_user_data(str(ctx.author.id))
            item_still_exists = any(item.get("unique_id") == item_id for item in seller_data["inventario"])
            
            if not item_still_exists:
                await interaction.response.send_message("❌ El vendedor ya no tiene este item", ephemeral=True)
                return
            
            # Realizar la transacción
            success_transfer, msg_transfer = await economy_system.transfer_item(
                str(ctx.author.id), buyer_id, item_id
            )
            
            if success_transfer:
                # Transferir el dinero
                await economy_system.remove_coins(buyer_id, precio)
                await economy_system.add_coins(str(ctx.author.id), precio)
                
                # Obtener datos actualizados
                seller_final = economy_system.get_user_data(str(ctx.author.id))
                buyer_final = economy_system.get_user_data(buyer_id)
                
                embed_success = discord.Embed(
                    title="✅ Venta Pública Completada",
                    description=(
                        f"**Item:** {item_encontrado['nombre']}\n"
                        f"**Precio:** {precio} monedas\n"
                        f"**Comprador:** {interaction.user.mention}\n"
                        f"**Vendedor:** {ctx.author.mention}"
                    ),
                    color=0x2ecc71
                )
                embed_success.add_field(
                    name="💰 Saldos actualizados",
                    value=(
                        f"**{ctx.author.display_name}:** {seller_final['monedas']} monedas (+{precio})\n"
                        f"**{interaction.user.display_name}:** {buyer_final['monedas']} monedas (-{precio})"
                    ),
                    inline=False
                )
                
                # Deshabilitar el botón
                for item in view.children:
                    item.disabled = True
                
                await interaction.response.edit_message(embed=embed_success, view=view)
            else:
                await interaction.response.send_message(f"❌ Error en la transacción: {msg_transfer}", ephemeral=True)
            
            # Limpiar venta activa
            if str(ctx.author.id) in active_sales:
                del active_sales[str(ctx.author.id)]
        
        async def timeout_callback():
            """Callback cuando el tiempo se agota"""
            # Solo procesar el timeout si la venta sigue activa
            if str(ctx.author.id) not in active_sales:
                return
                
            try:
                embed_expired = discord.Embed(
                    title="⏰ Oferta Expirada",
                    description="La oferta de venta ha expirado (60 segundos)",
                    color=0x95a5a6
                )
                
                # Buscar el mensaje original
                try:
                    message_obj = await ctx.channel.fetch_message(active_sales[str(ctx.author.id)]["message_id"])
                    await message_obj.edit(embed=embed_expired, view=None)
                except:
                    pass  # Si no se puede encontrar el mensaje, ignorar
                    
            except Exception as e:
                print(f"Error al editar mensaje expirado: {e}")
            
            # Limpiar venta activa
            if str(ctx.author.id) in active_sales:
                del active_sales[str(ctx.author.id)]
        
        buy_button = Button(label="💰 Comprar", style=discord.ButtonStyle.success)
        buy_button.callback = public_buy_callback
        view.add_item(buy_button)
        
        view.on_timeout = timeout_callback
        
        message = await ctx.send(embed=embed, view=view)
        active_sales[str(ctx.author.id)]["message_id"] = message.id
        
    except Exception as e:
        logger.error(f"Error en comando vender_publico: {e}")
        # Limpiar venta activa en caso de error
        if str(ctx.author.id) in active_sales:
            del active_sales[str(ctx.author.id)]
        await ctx.send("❌ Error al procesar la venta pública. Usa: `!vender_publico <item_id> <precio>`")
        
#regalo diario


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
                title="📅 Recompensa Diaria",
                description=f"{message}\n\n**Monedas actuales:** {user_data['monedas']}",
                color=0xf39c12
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(message)
            
    except Exception as e:
        logger.error(f"Error en comando diario: {e}")
        await ctx.send("❌ Error al reclamar la recompensa diaria")

# Comando para cancelar ventas activas
@bot.command(name='cancelar_venta')
async def cancelar_venta(ctx):
    """Cancelar tu venta activa"""
    try:
        if str(ctx.author.id) not in active_sales:
            await ctx.send("❌ No tienes ninguna venta activa para cancelar")
            return
        
        # Obtener información de la venta activa
        sale_info = active_sales[str(ctx.author.id)]
        
        # Eliminar la venta activa
        del active_sales[str(ctx.author.id)]
        
        await ctx.send("✅ Venta activa cancelada exitosamente")
        
    except Exception as e:
        logger.error(f"Error en comando cancelar_venta: {e}")
        await ctx.send("❌ Error al cancelar la venta activa")































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