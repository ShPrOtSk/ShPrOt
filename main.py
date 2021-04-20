import discord

from discord import utils

Client = discord.Client()

import config

intents = discord.Intents.all()


class MyClient(discord.Client):
    async def on_ready(self):

        print('Хм, нихило, но что-то не так. Иди проверь'.format (self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id) # Получаем объект канала
            message = await channel.fetch_message(payload.message_id) # Получаем оюъект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # Получаем объект пользователя который поставил реакцию

            try:
                emoji = str(payload.emoji) # Эмоджи которое выбрал пользователь
                role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # Реакция выбранной роли

                if(len([i for i in member.roles if i and i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print ('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Пользователь выбрал слишком много ролей {0.display_name}'.format(member))

            except KeyError as e:
                print ('[ERROR] Ляяяяяяя, крч, роль не найдена' + emoji)
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) # Получаем объект канала
        message = await channel.fetch_message(payload.message_id) # Получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # Получем объект пользователя который поставил реакцию

        try:
            emoji = str(payload.emoji) # Эмодзи которое выбрал пользователь
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # Объект выбранной роли

            await member.remove_roles(role)
            print(f'[SUCCES] Роль [1.Name] была снята у пользователя [0.display_name]')

        except KeyError as e:
            print('[ERROR] Роль не найдена или что-то там' + emoji)
        except Exception as e:
            print(repr(e))


client = MyClient(intents=intents)
client.run(config.TOKEN)

