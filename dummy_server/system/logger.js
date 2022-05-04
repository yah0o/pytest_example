class Logger {
    write(string) {
        console.log(`[${new Date().toISOString()}] ${string}`)
    }
} module.exports = Logger;
