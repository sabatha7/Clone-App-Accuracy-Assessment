const { Telegraf } = require('telegraf');
const fetch = require('node-fetch');
const fs = require('fs-extra');
const path = require('path');
const { exec } = require('child_process');
const os = require('os');
const mime = require('mime-types');

const API_ID = process.env.TELEGRAM_API_ID;  // Replace with your Telegram API ID
const API_HASH = process.env.TELEGRAM_API_HASH;  // Replace with your Telegram API hash
const BOT_TOKEN = process.env.NOCHAS_BOT;  // Replace with your bot's token

console.log('....');
const bot = new Telegraf(BOT_TOKEN);

bot.start(async (ctx) => {
    await ctx.reply("Bot has been started");
});

bot.on('text', async (ctx) => {
    try {
		const senderId = ctx.message.from.id;
        const cmdText = ctx.message.text;
        if (ctx.message.photo && ctx.message.photo.length === 1) {
            await persistPhoto(ctx);
        }
    } catch (error) {
        console.error("Error processing text message:", error);
    }
});

bot.on('photo', async (ctx) => {
    persistPhoto(ctx);
});

/**
 * Handles the persistence of a photo sent in a Telegram message.
 * 
 * This function performs the following steps:
 * 1. Extracts the photo from the message context.
 * 2. Retrieves the file link for the photo.
 * 3. Saves the photo to a local directory.
 * 4. Waits for a notification file to appear in a specified directory.
 * 5. Reads the notification file and sends a reply based on its contents.
 * 
 * @param {Object} ctx - The context object containing the message and other metadata.
 * @param {Object} ctx.message - The message object from the context.
 * @param {Array} ctx.message.photo - Array of photo objects in the message.
 * @param {Object} ctx.message.from - The sender of the message.
 * @param {string} ctx.message.from.id - The ID of the sender.
 * @param {string} ctx.message.from.username - The username of the sender.
 * @param {number} ctx.message.message_id - The ID of the message.
 * 
 * @returns {Promise<void>} - A promise that resolves when the photo has been processed.
 * 
 * @throws {Error} - Throws an error if there is an issue processing the photo or notification file.
 */
async function persistPhoto(ctx) {
    try {
        const photo = ctx.message.photo[0];
        const fileId = photo.file_id;
        const fileUrl = await bot.telegram.getFileLink(fileId);
        const timestamp = new Date().getTime();
        const fileName = `${ctx.message.from.id}_${timestamp}.jpg`;
        const filePath = path.join(__dirname, 'groups-task', fileName);

        const response = await fetch(fileUrl);
        const buffer = await response.buffer();
        await fs.outputFile(filePath, buffer);

        // await ctx.reply(`Photo saved to ${filePath}`);
        const notifyFilePath = path.join(__dirname, 'notify-groups-task', `${ctx.message.from.id}_${timestamp}.txt`);
        await new Promise(resolve => setTimeout(resolve, 19000)); // wait for 23 second before checking again
        if (fs.existsSync(notifyFilePath)) {
            try {
                message_id = ctx.message.message_id;
                const notifyData = (await fs.readFile(notifyFilePath, 'utf8')).split('|');
                console.log(notifyData);
                const winning = parseFloat(notifyData[0]);
                const won = parseFloat(notifyData[1]);
                if (winning > won && winning > 0.5) {
                    await ctx.reply(`⚽. @${ctx.message.from.username}`);
                } 
                if (won > winning && won > 0.5) {
                    await ctx.reply(`💃💰 mafias respira. @${ctx.message.from.username}`);
                }
                await fs.remove(notifyFilePath);
            } catch (error) {
                //console.error("Error processing notify file:", error);
                await fs.remove(notifyFilePath);
            }
        }
    } catch (error) {
        console.error("Error processing photo message:", error);
        // await ctx.reply("Failed to save the photo.");
    }
}



// Example Commands to test:
const commands = [
	'python app.py customer/task/image.jpg'
];

bot.launch();

