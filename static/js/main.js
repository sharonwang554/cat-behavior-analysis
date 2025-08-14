// Main JavaScript for Cat Behavior Analysis System

// Helper functions for determining CSS classes based on content
function getEmotionalStateClass(state) {
  if (!state) return "status-low";
  const lowerState = state.toLowerCase();
  if (lowerState.includes("playful") || lowerState.includes("expressive"))
    return "status-playful";
  if (lowerState.includes("stressed") || lowerState.includes("strained"))
    return "status-stressed";
  if (lowerState.includes("calm") || lowerState.includes("controlled"))
    return "status-calm";
  if (lowerState.includes("seeking") || lowerState.includes("attention"))
    return "status-seeking";
  if (lowerState.includes("serious") || lowerState.includes("formal"))
    return "status-serious";
  if (lowerState.includes("alert") || lowerState.includes("excited"))
    return "status-alert";
  if (lowerState.includes("relaxed") || lowerState.includes("content"))
    return "status-relaxed";
  return "status-medium";
}

function getActivityClass(activity) {
  if (!activity) return "status-low";
  const lowerActivity = activity.toLowerCase();
  if (lowerActivity.includes("high")) return "status-activity-high";
  if (lowerActivity.includes("medium")) return "status-activity-medium";
  if (lowerActivity.includes("low")) return "status-activity-low";
  return "status-low";
}

function getUrgencyClass(urgency) {
  if (!urgency) return "status-low";
  const lowerUrgency = urgency.toLowerCase();
  if (lowerUrgency.includes("high") || lowerUrgency.includes("urgent"))
    return "status-urgent";
  if (lowerUrgency.includes("low") || lowerUrgency.includes("very low"))
    return "status-normal";
  return "status-medium";
}

function getConfidenceClass(confidence) {
  if (!confidence) return "status-low";
  const lowerConf = confidence.toLowerCase();
  if (lowerConf.includes("high")) return "status-high";
  if (lowerConf.includes("medium")) return "status-medium";
  return "status-low";
}

// Initialize badge colors when page loads
document.addEventListener("DOMContentLoaded", function () {
  // Apply colors to all badges
  const emotionBadges = document.querySelectorAll('[id^="emotion-badge"]');
  emotionBadges.forEach((badge) => {
    const state = badge.textContent.trim();
    badge.className += " " + getEmotionalStateClass(state);
  });

  const activityBadges = document.querySelectorAll('[id^="activity-badge"]');
  activityBadges.forEach((badge) => {
    const activity = badge.textContent.trim();
    badge.className += " " + getActivityClass(activity);
  });

  const urgencyBadges = document.querySelectorAll('[id^="urgency-badge"]');
  urgencyBadges.forEach((badge) => {
    const urgency = badge.textContent.trim();
    badge.className += " " + getUrgencyClass(urgency);
  });

  const confidenceBadges = document.querySelectorAll(
    '[id^="confidence-badge"], [id$="confidence-badge"]'
  );
  confidenceBadges.forEach((badge) => {
    const confidence = badge.textContent.trim();
    badge.className += " " + getConfidenceClass(confidence);
  });
});

// File upload handling
function handleFileUpload(files) {
  const uploadArea = document.querySelector(".upload-area");
  const progressContainer = document.querySelector(".progress-container");

  if (files.length > 0) {
    // Show progress
    if (progressContainer) {
      progressContainer.style.display = "block";
    }

    // Simulate upload progress (replace with actual upload logic)
    let progress = 0;
    const progressBar = document.querySelector(".progress-fill");
    const interval = setInterval(() => {
      progress += Math.random() * 10;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
      }
      if (progressBar) {
        progressBar.style.width = progress + "%";
      }
    }, 200);
  }
}

// Drag and drop functionality
document.addEventListener("DOMContentLoaded", function () {
  const uploadArea = document.querySelector(".upload-area");

  if (uploadArea) {
    uploadArea.addEventListener("dragover", function (e) {
      e.preventDefault();
      uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", function (e) {
      e.preventDefault();
      uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", function (e) {
      e.preventDefault();
      uploadArea.classList.remove("dragover");
      const files = e.dataTransfer.files;
      handleFileUpload(files);
    });
  }
});
