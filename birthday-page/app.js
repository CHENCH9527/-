const canvas = document.querySelector("#scene");
const context = canvas.getContext("2d");
const subtitle = document.querySelector("#scene-subtitle");
const replayButton = document.querySelector("#replay");
const pauseButton = document.querySelector("#pause");
const passwordForm = document.querySelector("#password-form");
const passwordInput = document.querySelector("#password-input");
const passwordStatus = document.querySelector("#password-status");
const birthdayAudio = document.querySelector("#birthday-audio");

const DESIGN_WIDTH = 320;
const DESIGN_HEIGHT = 400;
const RENDER_SCALE = 2;
const WIDTH = DESIGN_WIDTH;
const HEIGHT = DESIGN_HEIGHT;
const LOOP_SECONDS = 36;
const PASSWORD = "1031";
const COLORS = {
  cyan: "#68e6e2",
  green: "#74f5a4",
  gold: "#f4c862",
  pink: "#ff4d8d",
  white: "#f9ffff",
  ink: "#071126",
  muted: "#a7b4c8",
};

const stars = Array.from({ length: 42 }, (_, index) => ({
  x: (index * 71 + 19) % WIDTH,
  y: (index * 43 + 13) % HEIGHT,
  size: index % 6 === 0 ? 2 : 1,
}));

let fireworks = [];
let confetti = [];
let animationStart = performance.now();
let pausedAt = null;
let lastFrame = performance.now();
let lastBurst = -1;
let passwordAccepted = false;
let audioStarted = false;

function clamp(value, min = 0, max = 1) {
  return Math.min(max, Math.max(min, value));
}

function ease(value) {
  const progress = clamp(value);
  return 1 - (1 - progress) ** 3;
}

function pixelText(text, x, y, size, color, stroke = COLORS.ink) {
  context.font = `700 ${size}px "Courier New", monospace`;
  context.textAlign = "center";
  context.textBaseline = "middle";
  context.lineWidth = 2;
  context.strokeStyle = stroke;
  context.strokeText(text, x, y);
  context.fillStyle = color;
  context.fillText(text, x, y);
}

function label(text, x, y, color = COLORS.muted, align = "left") {
  context.font = '10px "Courier New", monospace';
  context.textAlign = align;
  context.textBaseline = "middle";
  context.fillStyle = color;
  context.fillText(text, x, y);
}

function resetAnimation() {
  fireworks = [];
  confetti = [];
  lastBurst = -1;
}

function addBurst(x, y, color) {
  for (let index = 0; index < 18; index += 1) {
    const angle = (Math.PI * 2 * index) / 18;
    fireworks.push({
      x,
      y,
      vx: Math.cos(angle) * (18 + Math.random() * 28),
      vy: Math.sin(angle) * (18 + Math.random() * 28),
      life: 1,
      color,
    });
  }
}

function addConfetti() {
  const colors = [COLORS.pink, COLORS.cyan, COLORS.gold, COLORS.white];
  for (let index = 0; index < 28; index += 1) {
    confetti.push({
      x: Math.random() * WIDTH,
      y: 58,
      speed: 12 + Math.random() * 20,
      sway: Math.random() * 6,
      color: colors[index % colors.length],
    });
  }
}

function updateParticles(delta) {
  fireworks = fireworks.filter((particle) => particle.life > 0);
  fireworks.forEach((particle) => {
    particle.x += particle.vx * delta;
    particle.y += particle.vy * delta;
    particle.vy += 16 * delta;
    particle.life -= delta * 0.62;
  });
  confetti.forEach((piece) => {
    piece.y += piece.speed * delta;
    piece.x += Math.sin(piece.y * 0.04 + piece.sway) * delta * 12;
  });
  confetti = confetti.filter((piece) => piece.y < HEIGHT + 8);
}

function drawParticles() {
  fireworks.forEach((particle) => {
    context.globalAlpha = Math.max(0, particle.life);
    context.fillStyle = particle.color;
    context.fillRect(Math.round(particle.x), Math.round(particle.y), 3, 3);
  });
  confetti.forEach((piece) => {
    context.globalAlpha = 0.9;
    context.fillStyle = piece.color;
    context.fillRect(Math.round(piece.x), Math.round(piece.y), 3, 8);
  });
  context.globalAlpha = 1;
}

function drawBackground(seconds) {
  context.fillStyle = "#0c142d";
  context.fillRect(0, 0, WIDTH, HEIGHT);
  context.fillStyle = "#151e39";
  context.fillRect(0, 62, WIDTH, HEIGHT - 62);

  context.strokeStyle = "rgba(104, 230, 226, 0.12)";
  context.lineWidth = 1;
  for (let x = 20; x < WIDTH; x += 20) {
    context.beginPath();
    context.moveTo(x, 62);
    context.lineTo(x, HEIGHT);
    context.stroke();
  }
  for (let y = 82; y < HEIGHT; y += 20) {
    context.beginPath();
    context.moveTo(0, y);
    context.lineTo(WIDTH, y);
    context.stroke();
  }

  const scanY = 62 + ((seconds * 24) % (HEIGHT - 62));
  context.fillStyle = "rgba(104, 230, 226, 0.15)";
  context.fillRect(0, scanY, WIDTH, 3);

  stars.forEach((star, index) => {
    context.globalAlpha = 0.25 + 0.55 * Math.abs(Math.sin(seconds * 1.2 + index));
    context.fillStyle = index % 4 === 0 ? COLORS.gold : "#dbe4ff";
    context.fillRect(star.x, star.y + 62, star.size, star.size);
  });
  context.globalAlpha = 1;

  context.fillStyle = COLORS.cyan;
  context.fillRect(12, 16, 4, 18);
  context.fillRect(12, 16, 36, 4);
  context.fillRect(WIDTH - 48, HEIGHT - 18, 36, 4);
  context.fillRect(WIDTH - 16, HEIGHT - 36, 4, 22);
  label("SECURE CHANNEL // 04", 22, 28, COLORS.cyan);
  label("HANGZHOU // NIGHT OPS", 22, 48);
  label("SIGNAL: STABLE", 216, 28, COLORS.gold);
}

function drawUnlockBackdrop(seconds) {
  const phase = seconds - 22.2;
  if (phase <= 0) return;

  const pulse = 0.5 + 0.5 * Math.sin(phase * 4);
  const sweepY = 62 + ((phase * 52) % (HEIGHT - 62));
  const markerX = (phase * 72) % (WIDTH + 24) - 12;

  context.save();
  context.fillStyle = "rgba(116, 245, 164, 0.14)";
  context.fillRect(0, sweepY, WIDTH, 2);

  context.strokeStyle = `rgba(116, 245, 164, ${0.12 + pulse * 0.2})`;
  context.lineWidth = 2;
  context.strokeRect(10, 70, WIDTH - 20, HEIGHT - 90);

  context.fillStyle = COLORS.green;
  context.globalAlpha = 0.45 + pulse * 0.4;
  context.fillRect(markerX, HEIGHT - 24, 12, 3);
  context.fillRect(WIDTH - markerX - 12, 74, 12, 3);
  context.restore();
}

function drawActionEntry(seconds) {
  const progress = ease((seconds - 2.8) / 3.8);
  if (progress <= 0 || seconds >= 7.2) return;

  context.globalAlpha = Math.min(1, progress * 1.5);
  context.fillStyle = "rgba(7, 17, 38, 0.92)";
  context.fillRect(28, 86, 264, 190);
  context.strokeStyle = COLORS.cyan;
  context.lineWidth = 2;
  context.strokeRect(28, 86, 264, 190);

  pixelText("ENTERING ACTION", 160, 110, 16, COLORS.cyan);
  label("OPERATION: BIRTHDAY", 48, 140, COLORS.gold);
  label("TARGET: 灯芯", 48, 158, COLORS.white);
  label("OBJECTIVE: OPEN THE SAFE", 48, 176, COLORS.white);
  label("ROUTE: HANGZHOU / NIGHT OPS", 48, 194);

  context.strokeStyle = "rgba(104, 230, 226, 0.55)";
  context.strokeRect(177, 135, 92, 78);
  context.strokeStyle = "rgba(244, 200, 98, 0.65)";
  context.beginPath();
  context.moveTo(188, 196);
  context.lineTo(218, 174);
  context.lineTo(248, 185);
  context.lineTo(260, 148);
  context.stroke();
  context.fillStyle = COLORS.pink;
  context.fillRect(255, 143, 8, 8);
  context.fillStyle = COLORS.green;
  context.fillRect(184 + progress * 68, 190, 6, 6);

  context.fillStyle = COLORS.green;
  context.fillRect(48, 229, 210 * progress, 6);
  context.strokeStyle = COLORS.muted;
  context.strokeRect(48, 229, 210, 6);
  label(`ACTION ENTRY ${Math.floor(progress * 100)}%`, 48, 250, COLORS.green);
  context.globalAlpha = 1;
}

function drawSafeDiscovery(seconds) {
  const progress = ease((seconds - 6.2) / 4.2);
  if (progress <= 0 || seconds >= 11.5) return;

  context.globalAlpha = Math.min(1, progress * 1.5);
  context.fillStyle = "rgba(7, 17, 38, 0.88)";
  context.fillRect(38, 112, 244, 154);
  context.strokeStyle = COLORS.gold;
  context.lineWidth = 2;
  context.strokeRect(38, 112, 244, 154);
  pixelText("SEARCHING AREA", 160, 136, 16, COLORS.gold);

  const reticleX = 62 + progress * 194;
  const reticleY = 187 + Math.sin(seconds * 2) * 18;
  context.strokeStyle = COLORS.cyan;
  context.strokeRect(70, 156, 180, 72);
  context.strokeStyle = COLORS.pink;
  context.strokeRect(reticleX - 12, reticleY - 12, 24, 24);
  context.fillStyle = COLORS.pink;
  context.fillRect(reticleX - 2, reticleY - 2, 4, 4);

  if (progress > 0.55) {
    context.fillStyle = "rgba(244, 200, 98, 0.18)";
    context.fillRect(185, 168, 54, 44);
    context.strokeStyle = COLORS.gold;
    context.strokeRect(185, 168, 54, 44);
    label("SAFE", 212, 190, COLORS.gold, "center");
  }
  label(progress > 0.65 ? "SIGNAL DETECTED" : "SCANNING...", 58, 244, progress > 0.65 ? COLORS.green : COLORS.muted);
  label("DISTANCE: " + Math.floor(180 - progress * 90) + "M", 190, 244, COLORS.muted);
  context.globalAlpha = 1;
}

function drawSafeHack(seconds) {
  const appear = ease((seconds - 10.8) / 0.7);
  if (appear <= 0 || seconds >= 22.2) return;

  const x = 18;
  const y = 92;
  const width = 284;
  const height = 215;
  const entered = Math.min(4, passwordInput.value.length);
  const unlock = entered / 4;
  const opening = passwordAccepted ? 1 : 0;

  context.globalAlpha = appear;
  context.fillStyle = "#192638";
  context.fillRect(x, y, width, height);
  context.strokeStyle = "#8493a6";
  context.lineWidth = 2;
  context.strokeRect(x, y, width, height);
  context.fillStyle = "#0d1728";
  context.fillRect(x + 8, y + 32, width - 16, height - 42);
  context.strokeStyle = "rgba(132, 147, 166, 0.6)";
  context.strokeRect(x + 8, y + 32, width - 16, height - 42);

  label("PASSWORD ENTRY", x + 12, y + 15, COLORS.white);
  label("PASSWORD GRID", x + 17, y + 50, COLORS.muted);

  const symbols = ["2", "0", "+", "&", ")", "K", "9", "4", "M", "9", "L", "(", "^", "=", "6", "D", "~", "&", "2", "@"];
  symbols.forEach((symbol, index) => {
    const column = index % 5;
    const row = Math.floor(index / 5);
    const cellX = x + 18 + column * 42;
    const cellY = y + 54 + row * 27;
    context.fillStyle = row === 2 && index === 12 ? "#1c443e" : "#111d2e";
    context.fillRect(cellX, cellY, 36, 22);
    label(symbol, cellX + 18, cellY + 11, row === 2 && index === 12 ? COLORS.green : COLORS.muted, "center");
  });

  const lockWidth = 152;
  context.strokeStyle = COLORS.green;
  context.strokeRect(x + 14, y + 126, lockWidth, 30);
  context.fillStyle = "rgba(116, 245, 164, 0.12)";
  context.fillRect(x + 14, y + 126, lockWidth * unlock, 30);
  for (let index = 0; index < 4; index += 1) {
    pixelText(index < entered ? PASSWORD[index] : "_", x + 34 + index * 32, y + 141, 14, index < entered ? COLORS.green : COLORS.muted);
  }

  context.strokeStyle = COLORS.muted;
  context.strokeRect(x + 14, y + 168, 190, 8);
  context.fillStyle = COLORS.green;
  context.fillRect(x + 14, y + 168, 190 * unlock, 8);
  label(`PASSWORD INPUT ${entered}/4`, x + 14, y + 192, COLORS.green);

  const successX = x + 218;
  const successY = y + 75;
  context.strokeStyle = opening > 0 ? COLORS.green : "rgba(116, 245, 164, 0.35)";
  context.lineWidth = 2;
  context.beginPath();
  context.arc(successX, successY, 35, 0, Math.PI * 2);
  context.stroke();
  if (opening > 0) {
    context.fillStyle = "rgba(116, 245, 164, 0.22)";
    context.beginPath();
    context.arc(successX, successY, 28, 0, Math.PI * 2);
    context.fill();
    pixelText("破解成功", successX, successY, 12, COLORS.green);
  } else {
    label("LOCKED", successX, successY, COLORS.muted, "center");
  }
  context.globalAlpha = 1;
}

function drawBirthdaySequence(seconds) {
  const phase = seconds - 22.2;
  if (phase <= 0 || phase >= 8) return;

  const reveal = ease(Math.min(phase / 1.2, 1));
  const panelX = 32;
  const panelY = 88;
  const panelWidth = 256;
  const panelHeight = 190;
  context.globalAlpha = reveal;
  context.fillStyle = "rgba(7, 17, 38, 0.94)";
  context.fillRect(panelX, panelY, panelWidth, panelHeight);
  context.strokeStyle = COLORS.green;
  context.lineWidth = 2;
  context.strokeRect(panelX, panelY, panelWidth, panelHeight);

  const greetingDuration = 1.8;
  if (phase < greetingDuration) {
    pixelText("生日快乐！", 160, 168, 22, COLORS.gold);
    context.globalAlpha = 1;
    return;
  }

  const messages = [
    ["愿你新的一岁，开心常驻，烦恼退散，", "一切都顺顺利利。"],
    ["祝：灯芯，天天开心！"],
  ];
  const stepDuration = 2.1;
  const playback = phase - greetingDuration;
  const messageIndex = Math.min(
    messages.length - 1,
    Math.floor(playback / stepDuration),
  );
  const stepProgress = playback - messageIndex * stepDuration;
  const messageAlpha = clamp(
    Math.min(stepProgress / 0.35, (stepDuration - stepProgress) / 0.35),
  );
  const messageProgress = clamp(playback / (stepDuration * messages.length));

  context.globalAlpha = messageAlpha;
  messages[messageIndex].forEach((line, index) => {
    pixelText(line, 160, 194 + index * 25, 11, COLORS.white);
  });
  context.globalAlpha = reveal;
  context.strokeStyle = COLORS.muted;
  context.strokeRect(58, 250, 204, 8);
  context.fillStyle = COLORS.green;
  context.fillRect(58, 250, 204 * messageProgress, 8);
  context.globalAlpha = 1;
}

function drawBirthdayCake(seconds) {
  const reveal = ease((seconds - 30.2) / 2.2);
  if (reveal <= 0) return;
  const bounce = Math.sin(seconds * 3) * 2;
  const cakeY = 302 - reveal * 16 + bounce;

  context.globalAlpha = reveal;
  pixelText("生日快乐！", 160, 244, 15, COLORS.gold);

  context.fillStyle = "#fff4d6";
  context.fillRect(84, cakeY + 62, 152, 8);
  context.strokeStyle = COLORS.gold;
  context.lineWidth = 2;
  context.strokeRect(84, cakeY + 62, 152, 8);

  context.fillStyle = COLORS.pink;
  context.fillRect(96, cakeY + 18, 128, 46);
  context.strokeStyle = COLORS.white;
  context.strokeRect(96, cakeY + 18, 128, 46);
  context.fillStyle = "#ff9fc9";
  context.fillRect(106, cakeY + 42, 108, 22);

  context.fillStyle = "#fff4d6";
  context.fillRect(108, cakeY, 104, 26);
  context.strokeStyle = COLORS.gold;
  context.strokeRect(108, cakeY, 104, 26);
  context.fillStyle = COLORS.pink;
  context.fillRect(116, cakeY + 20, 12, 9);
  context.fillRect(152, cakeY + 20, 12, 9);
  context.fillRect(188, cakeY + 20, 12, 9);

  [128, 160, 192].forEach((candleX, index) => {
    context.fillStyle = index === 1 ? COLORS.cyan : COLORS.gold;
    context.fillRect(candleX - 4, cakeY - 28, 8, 28);
    context.fillStyle = COLORS.gold;
    context.fillRect(candleX - 3, cakeY - 37 - (index % 2) * 3, 6, 9);
  });

  context.globalAlpha = 1;
}

function drawActionEntry(seconds) {
  if (seconds >= 2.8 && seconds < 7.2) {
    const progress = ease((seconds - 2.8) / 3.8);
    context.fillStyle = "rgba(7, 17, 38, 0.92)";
    context.fillRect(28, 86, 264, 190);
    context.strokeStyle = COLORS.cyan;
    context.lineWidth = 2;
    context.strokeRect(28, 86, 264, 190);
    pixelText("ENTERING ACTION", 160, 110, 16, COLORS.cyan);
    label("OPERATION: BIRTHDAY", 48, 140, COLORS.gold);
    label("TARGET: 灯芯", 48, 158, COLORS.white);
    label("OBJECTIVE: OPEN THE SAFE", 48, 176, COLORS.white);
    label("ROUTE: HANGZHOU / NIGHT OPS", 48, 194);
    context.strokeStyle = "rgba(104, 230, 226, 0.55)";
    context.strokeRect(177, 135, 92, 78);
    context.strokeStyle = "rgba(244, 200, 98, 0.65)";
    context.beginPath();
    context.moveTo(188, 196);
    context.lineTo(218, 174);
    context.lineTo(248, 185);
    context.lineTo(260, 148);
    context.stroke();
    context.fillStyle = COLORS.pink;
    context.fillRect(255, 143, 8, 8);
    context.fillStyle = COLORS.green;
    context.fillRect(184 + progress * 68, 190, 6, 6);
    context.fillStyle = COLORS.green;
    context.fillRect(48, 229, 210 * progress, 6);
    context.strokeStyle = COLORS.muted;
    context.strokeRect(48, 229, 210, 6);
    label(`ACTION ENTRY ${Math.floor(progress * 100)}%`, 48, 250, COLORS.green);
  }
}

function drawSafeDiscovery(seconds) {
  if (seconds < 6.5 || seconds >= 11.5) return;
  const progress = ease((seconds - 6.5) / 5);
  context.fillStyle = "rgba(7, 17, 38, 0.9)";
  context.fillRect(38, 112, 244, 154);
  context.strokeStyle = COLORS.gold;
  context.lineWidth = 2;
  context.strokeRect(38, 112, 244, 154);
  pixelText("SEARCHING AREA", 160, 136, 16, COLORS.gold);
  const reticleX = 62 + progress * 194;
  const reticleY = 187 + Math.sin(seconds * 2) * 18;
  context.strokeStyle = COLORS.cyan;
  context.strokeRect(70, 156, 180, 72);
  context.strokeStyle = COLORS.pink;
  context.strokeRect(reticleX - 12, reticleY - 12, 24, 24);
  context.fillStyle = COLORS.pink;
  context.fillRect(reticleX - 2, reticleY - 2, 4, 4);
  if (progress > 0.55) {
    context.fillStyle = "rgba(244, 200, 98, 0.18)";
    context.fillRect(185, 168, 54, 44);
    context.strokeStyle = COLORS.gold;
    context.strokeRect(185, 168, 54, 44);
    label("SAFE", 212, 190, COLORS.gold, "center");
  }
  label(progress > 0.65 ? "SIGNAL DETECTED" : "SCANNING...", 58, 244, progress > 0.65 ? COLORS.green : COLORS.muted);
  label(`DISTANCE: ${Math.floor(180 - progress * 90)}M`, 190, 244);
}

function drawMissionText(seconds) {
  if (seconds < 2.8) {
    pixelText("OPERATION: BIRTHDAY", 160, 104, 16, COLORS.cyan);
    pixelText("TARGET: 灯芯", 160, 130, 13, COLORS.gold);
    label("MISSION BRIEFING READY", 104, 360, COLORS.muted);
  } else if (seconds >= 7.2 && seconds < 11.5) {
    pixelText("SAFE LOCATED", 160, 102, 18, COLORS.gold);
    label("OBJECTIVE: APPROACH THE SAFE", 78, 360, COLORS.muted);
  } else if (seconds >= 11.5 && seconds < 21.3) {
    pixelText("BYPASSING SECURITY", 160, 102, 15, COLORS.cyan);
    label("PASSWORD ENTRY // MANUAL INPUT", 70, 360, COLORS.gold);
  } else if (seconds >= 21.3 && seconds < 22.2) {
    pixelText("SAFE UNLOCKED", 160, 102, 18, COLORS.green);
  } else if (seconds >= 22.2 && seconds < 30.2) {
    pixelText("BIRTHDAY MESSAGE", 160, 102, 16, COLORS.pink);
  }
}

function drawFinalPanel(seconds) {
  if (seconds < 33.2) return;
  context.fillStyle = "rgba(5, 10, 24, 0.9)";
  context.fillRect(35, 70, 250, 72);
  context.strokeStyle = COLORS.green;
  context.lineWidth = 2;
  context.strokeRect(35, 70, 250, 72);
  pixelText("MISSION COMPLETE", 160, 90, 14, COLORS.green);
  pixelText("祝：灯芯，天天开心！", 160, 118, 17, COLORS.gold);
}

function updateSubtitle(seconds) {
  if (seconds < 2.8) subtitle.textContent = "生日特别行动简报";
  else if (seconds < 6.5) subtitle.textContent = "正在进入行动界面";
  else if (seconds < 11.5) subtitle.textContent = "搜索并发现保险箱";
  else if (seconds < 21.3) subtitle.textContent = "正在破解保险密码 1031";
  else if (seconds < 22.2) subtitle.textContent = "保险箱已解锁";
  else if (seconds < 24) subtitle.textContent = "生日祝福已解锁";
  else if (seconds < 30.2) subtitle.textContent = "生日祝福语正在依次播放";
  else if (seconds < 33.2) subtitle.textContent = "生日祝福正在送达";
  else subtitle.textContent = "任务完成，生日快乐";
}

function updatePasswordForm(seconds) {
  const visible = seconds >= 10.8 && seconds < 22.2 && !passwordAccepted;
  passwordForm.hidden = !visible;
}

function render(seconds) {
  context.setTransform(RENDER_SCALE, 0, 0, RENDER_SCALE, 0, 0);
  context.imageSmoothingEnabled = false;
  context.clearRect(0, 0, WIDTH, HEIGHT);
  drawBackground(seconds);
  drawUnlockBackdrop(seconds);
  drawActionEntry(seconds);
  drawSafeDiscovery(seconds);
  drawSafeHack(seconds);
  drawBirthdaySequence(seconds);
  drawBirthdayCake(seconds);
  drawFinalPanel(seconds);
  drawParticles();
  updateSubtitle(seconds);
  updatePasswordForm(seconds);
}

function frame(now) {
  const delta = Math.min(0.05, (now - lastFrame) / 1000);
  lastFrame = now;
  if (pausedAt === null) {
    const seconds = ((now - animationStart) / 1000) % LOOP_SECONDS;
    const burstWave = Math.floor(seconds * 0.8);
    if (burstWave !== lastBurst) {
      lastBurst = burstWave;
      if (seconds > 21.3) addBurst(160, 210, burstWave % 2 ? COLORS.cyan : COLORS.gold);
      if (seconds > 30.2) addConfetti();
    }
    updateParticles(delta);
    render(seconds);
  }
  requestAnimationFrame(frame);
}

replayButton.addEventListener("click", () => {
  animationStart = performance.now();
  pausedAt = null;
  passwordAccepted = false;
  audioStarted = false;
  passwordInput.value = "";
  passwordStatus.textContent = "";
  birthdayAudio.pause();
  birthdayAudio.currentTime = 0;
  pauseButton.textContent = "Ⅱ";
  pauseButton.setAttribute("aria-label", "暂停动画");
  pauseButton.title = "暂停动画";
  resetAnimation();
});

passwordForm.addEventListener("submit", (event) => {
  event.preventDefault();
  if (passwordInput.value !== PASSWORD) {
    passwordStatus.textContent = "密码错误";
    passwordInput.select();
    return;
  }

  passwordAccepted = true;
  audioStarted = true;
  passwordStatus.textContent = "";
  pausedAt = null;
  pauseButton.textContent = "Ⅱ";
  pauseButton.setAttribute("aria-label", "暂停动画");
  pauseButton.title = "暂停动画";
  animationStart = performance.now() - 22.2 * 1000;
  resetAnimation();
  birthdayAudio.currentTime = 0;
  birthdayAudio.play().catch(() => {
    passwordStatus.textContent = "请点击页面后播放祝福音频";
  });
});

pauseButton.addEventListener("click", () => {
  if (pausedAt === null) {
    pausedAt = performance.now();
    if (audioStarted) birthdayAudio.pause();
    pauseButton.textContent = "▶";
    pauseButton.setAttribute("aria-label", "继续播放");
    pauseButton.title = "继续播放";
  } else {
    animationStart += performance.now() - pausedAt;
    pausedAt = null;
    if (audioStarted) birthdayAudio.play().catch(() => {});
    pauseButton.textContent = "Ⅱ";
    pauseButton.setAttribute("aria-label", "暂停动画");
    pauseButton.title = "暂停动画";
  }
});

requestAnimationFrame(frame);
