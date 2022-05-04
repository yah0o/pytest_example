class Timer {
    static timeout(seconds, run) {
        setTimeout(() => run(), seconds * 1000);
    }
} module.exports = Timer;