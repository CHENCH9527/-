const canvas = document.querySelector("#scene");
const context = canvas.getContext("2d");
const subtitle = document.querySelector("#scene-subtitle");
const replayButton = document.querySelector("#replay");
const pauseButton = document.querySelector("#pause");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;
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
  context.lineWidth = 3;
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
  context.fillStyle = "rgba(104, 230, 226, 0.08)";
  context.fillRect(0, scanY, WIDTH, 2);

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
  label("TARGET: xx", 48, 158, COLORS.white);
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
  const unlock = clamp((seconds - 11.5) / 10);
  const entered = Math.min(4, Math.floor(unlock * 5));
  const opening = ease((seconds - 21.3) / 1.3);

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

  label("破解方法：当绿色的密码达到中央时，按空格锁定密码。", x + 12, y + 15, COLORS.white);
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
  label(`AUTO DECRYPTING... ${Math.floor(unlock * 100)}%`, x + 14, y + 192, COLORS.green);

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

function drawBirthdayUnlock(seconds) {
  const reveal = ease((seconds - 22.2) / 1.2);
  if (reveal <= 0 || seconds >= 29.2) return;

  context.globalAlpha = reveal;
  context.fillStyle = "rgba(7, 17, 38, 0.94)";
  context.fillRect(28, 88, 264, 190);
  context.strokeStyle = COLORS.green;
  context.lineWidth = 2;
  context.strokeRect(28, 88, 264, 190);

  pixelText("BIRTHDAY UNLOCKED", 160, 116, 14, COLORS.green);
  pixelText("生日祝福已解锁", 160, 150, 20, COLORS.gold);
  label("PASSWORD ACCEPTED // MESSAGE CHANNEL OPEN", 160, 178, COLORS.cyan, "center");

  const messageStart = 23.8;
  const messageProgress = clamp((seconds - messageStart) / 5.2);
  const messages = [
    "xx，生日快乐！",
    "愿新的一岁，平安顺利，常有好心情。",
    "愿每一个期待，都能收到温柔回应。",
  ];
  const visibleCount = Math.min(messages.length, Math.floor(messageProgress * (messages.length + 1)));
  messages.slice(0, visibleCount).forEach((message, index) => {
    pixelText(message, 160, 210 + index * 22, index === 0 ? 15 : 10, index === 0 ? COLORS.pink : COLORS.white);
  });

  context.strokeStyle = COLORS.muted;
  context.strokeRect(58, 254, 204, 8);
  context.fillStyle = COLORS.green;
  context.fillRect(58, 254, 204 * messageProgress, 8);
  label(`MESSAGE PLAYBACK ${Math.floor(messageProgress * 100)}%`, 160, 272, COLORS.green, "center");
  context.globalAlpha = 1;
}

function drawPersonAndSign(seconds) {
  const reveal = ease((seconds - 29.2) / 2.2);
  if (reveal <= 0) return;
  const y = 347 - reveal * 23;

  context.globalAlpha = reveal;
  context.fillStyle = "#ffcf9a";
  context.fillRect(46, y - 44, 18, 18);
  context.fillStyle = "#202a44";
  context.fillRect(42, y - 48, 26, 8);
  context.fillRect(40, y - 26, 30, 38);
  context.fillStyle = COLORS.cyan;
  context.fillRect(47, y - 22, 16, 22);
  context.fillStyle = COLORS.pink;
  context.fillRect(43, y + 10, 10, 28);
  context.fillRect(58, y + 10, 10, 28);
  context.fillStyle = "#ffcf9a";
  context.fillRect(67, y - 18, 24, 7);

  context.fillStyle = "#fff4d6";
  context.fillRect(88, y - 25, 198, 58);
  context.strokeStyle = COLORS.gold;
  context.lineWidth = 2;
  context.strokeRect(88, y - 25, 198, 58);
  pixelText("祝你生日快乐！", 187, y - 4, 14, COLORS.pink, "#5f1029");
  label("愿新的一岁，天天都有好事发生", 187, y + 18, "#5f1029", "center");
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
    label("TARGET: xx", 48, 158, COLORS.white);
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
    pixelText("TARGET: xx", 160, 130, 13, COLORS.gold);
    label("MISSION BRIEFING READY", 104, 360, COLORS.muted);
  } else if (seconds >= 7.2 && seconds < 11.5) {
    pixelText("SAFE LOCATED", 160, 102, 18, COLORS.gold);
    label("OBJECTIVE: APPROACH THE SAFE", 78, 360, COLORS.muted);
  } else if (seconds >= 11.5 && seconds < 21.3) {
    pixelText("BYPASSING SECURITY", 160, 102, 15, COLORS.cyan);
    label("AUTO DECRYPTING // PASSWORD: 1031", 70, 360, COLORS.gold);
  } else if (seconds >= 21.3 && seconds < 22.2) {
    pixelText("SAFE UNLOCKED", 160, 102, 18, COLORS.green);
  } else if (seconds >= 22.2 && seconds < 29.2) {
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
  pixelText("xx，生日快乐！", 160, 118, 19, COLORS.gold);
}

function updateSubtitle(seconds) {
  if (seconds < 2.8) subtitle.textContent = "生日特别行动简报";
  else if (seconds < 6.5) subtitle.textContent = "正在进入行动界面";
  else if (seconds < 11.5) subtitle.textContent = "搜索并发现保险箱";
  else if (seconds < 21.3) subtitle.textContent = "正在破解保险密码 1031";
  else if (seconds < 22.2) subtitle.textContent = "保险箱已解锁";
  else if (seconds < 24) subtitle.textContent = "生日祝福已解锁";
  else if (seconds < 29.2) subtitle.textContent = "正在播放生日文案";
  else if (seconds < 33.2) subtitle.textContent = "生日祝福正在送达";
  else subtitle.textContent = "任务完成，生日快乐";
}

function render(seconds) {
  context.imageSmoothingEnabled = false;
  drawBackground(seconds);
  drawActionEntry(seconds);
  drawSafeDiscovery(seconds);
  drawSafeHack(seconds);
  drawBirthdayUnlock(seconds);
  drawPersonAndSign(seconds);
  drawFinalPanel(seconds);
  drawParticles();
  updateSubtitle(seconds);
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
      if (seconds > 29.2) addConfetti();
    }
    updateParticles(delta);
    render(seconds);
  }
  requestAnimationFrame(frame);
}

replayButton.addEventListener("click", () => {
  animationStart = performance.now();
  pausedAt = null;
  pauseButton.textContent = "Ⅱ";
  pauseButton.setAttribute("aria-label", "暂停动画");
  pauseButton.title = "暂停动画";
  resetAnimation();
});

pauseButton.addEventListener("click", () => {
  if (pausedAt === null) {
    pausedAt = performance.now();
    pauseButton.textContent = "▶";
    pauseButton.setAttribute("aria-label", "继续播放");
    pauseButton.title = "继续播放";
  } else {
    animationStart += performance.now() - pausedAt;
    pausedAt = null;
    pauseButton.textContent = "Ⅱ";
    pauseButton.setAttribute("aria-label", "暂停动画");
    pauseButton.title = "暂停动画";
  }
});

requestAnimationFrame(frame);
