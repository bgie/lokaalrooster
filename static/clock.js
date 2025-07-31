let nextRefreshTime = null;

function timeStrToDate(timeStr) {
    const now = new Date();
    return new Date(now.toDateString() + ' ' + timeStr);
}

function calculateNextRefreshTime() {
    const now = new Date();
    const eventTimes = [];

    // 1. Get all start and end times from the schedule list
    document.querySelectorAll('.schedule-entry .class-time').forEach(el => {
        const parts = el.textContent.split(' - ');
        if (parts.length === 2) {
            eventTimes.push(timeStrToDate(parts[0]));
            eventTimes.push(timeStrToDate(parts[1]));
        }
    });

    // 2. Get animation end time if break gif is present
    const breakGif = document.querySelector('.break-gif');
    if (breakGif) {
        const container = document.getElementById('progress-container');
        if (container) {
            const startTimeStr = container.dataset.startTime;
            const startTime = timeStrToDate(startTimeStr);
            const animationEndTime = new Date(startTime.getTime() + 60000); // 1 minute after start
            eventTimes.push(animationEndTime);
        }
    }

    // Find the soonest future event time
    const futureEvents = eventTimes
        .filter(t => t > now) // Only consider future times
        .sort((a, b) => a - b); // Sort chronologically

    if (futureEvents.length > 0) {
        nextRefreshTime = futureEvents[0];
    }
}

function updateClock() {
    const now = new Date();

    if (nextRefreshTime && now >= nextRefreshTime) {
        window.location.reload();
        return;
    }

    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('clock').innerHTML = `${hours}:${minutes}<span class="clock-seconds">:${seconds}</span>`;
    updateProgressBar();
}

function updateProgressBar() {
    const container = document.getElementById('progress-container');
    if (!container) {
        return; // No progress bar on this page
    }

    const startTimeStr = container.dataset.startTime;
    const endTimeStr = container.dataset.endTime;

    const now = new Date();
    // Create Date objects for today with the given times from the schedule.
    const startTime = new Date(now.toDateString() + ' ' + startTimeStr);
    const endTime = new Date(now.toDateString() + ' ' + endTimeStr);

    // This logic assumes start and end times are on the same day.
    const totalDuration = (endTime - startTime) / 1000; // duration in seconds
    const elapsed = (now - startTime) / 1000; // elapsed time in seconds

    if (totalDuration <= 0) {
        return; // Avoid division by zero or negative duration
    }

    let progress = (elapsed / totalDuration) * 100;

    // Clamp progress to be between 0% and 100%
    progress = Math.max(0, Math.min(100, progress));

    const fill = document.getElementById('progress-bar-fill');
    if (fill) {
        fill.style.width = progress + '%';
    }
}

calculateNextRefreshTime();
setInterval(updateClock, 1000);
updateClock(); // Initial call to display clock immediately
