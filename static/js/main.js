/**
 * 100% HUMANITY — Responsive Enhancements, Lightbox & Modal Controls
 */
let currentLightboxIndex = 0;
let currentLightboxItems = [];

window.openLightboxGallery = function (items, index) {
  if (!items || items.length === 0) return;
  currentLightboxItems = items;
  currentLightboxIndex = index || 0;
  window.renderLightboxSlide();
  const modal = document.getElementById("lightbox-modal");
  if (modal) modal.classList.remove("hidden");
};

window.openSingleLightbox = function (imgUrl, caption, albumTitle) {
  const modal = document.getElementById("lightbox-modal");
  const imgEl = document.getElementById("lightbox-image");
  const albumEl = document.getElementById("lightbox-album-title");
  const counterEl = document.getElementById("lightbox-counter");
  const capEl = document.getElementById("lightbox-caption");
  const creditEl = document.getElementById("lightbox-credit");
  if (!modal || !imgEl) return;

  currentLightboxItems = [{
    src: imgUrl,
    alt: caption,
    title: caption,
    albumTitle: albumTitle || "Photo Gallery",
    caption: caption
  }];
  currentLightboxIndex = 0;

  imgEl.src = imgUrl;
  imgEl.alt = caption;
  if (albumEl) albumEl.textContent = albumTitle || "Photo Gallery";
  if (counterEl) counterEl.textContent = "";
  if (capEl) capEl.textContent = caption || "";
  if (creditEl) creditEl.textContent = "";
  modal.classList.remove("hidden");
};

window.renderLightboxSlide = function () {
  if (!currentLightboxItems || currentLightboxItems.length === 0) return;
  const item = currentLightboxItems[currentLightboxIndex];
  const imgEl = document.getElementById("lightbox-image");
  const albumEl = document.getElementById("lightbox-album-title");
  const counterEl = document.getElementById("lightbox-counter");
  const capEl = document.getElementById("lightbox-caption");
  const creditEl = document.getElementById("lightbox-credit");

  if (imgEl && item) {
    imgEl.src = item.src || item.imageUrl || "";
    imgEl.alt = item.alt || item.title || "";
  }
  if (albumEl && item) {
    albumEl.textContent = item.albumTitle || item.title || "Photo Gallery";
  }
  if (counterEl) {
    counterEl.textContent = `Photo ${currentLightboxIndex + 1} of ${currentLightboxItems.length}`;
  }
  if (capEl && item) {
    capEl.textContent = item.caption || item.title || "";
  }
  if (creditEl && item) {
    creditEl.textContent = item.credit ? `Photo credit: ${item.credit}` : "";
  }
};

window.stepLightbox = function (delta) {
  if (!currentLightboxItems || currentLightboxItems.length === 0) return;
  const len = currentLightboxItems.length;
  currentLightboxIndex = (currentLightboxIndex + delta + len) % len;
  window.renderLightboxSlide();
};

window.closeLightbox = function () {
  const modal = document.getElementById("lightbox-modal");
  if (modal) modal.classList.add("hidden");
};

window.closeGenericModal = function () {
  const modal = document.getElementById("generic-modal");
  if (modal) modal.classList.add("hidden");
};

/**
 * Global Floating Toast Notification System
 */
window.showToast = function (message, type) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "fixed bottom-5 right-5 z-50 space-y-2.5 max-w-sm w-full pointer-events-none px-4 sm:px-0";
    container.setAttribute("aria-live", "polite");
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  const isError = type === "error";
  const isWarning = type === "warning";

  let bgClass = "bg-[#1B365D] border-emerald-400 text-white";
  let icon = "✓";
  if (isError) {
    bgClass = "bg-rose-900 border-rose-400 text-white";
    icon = "✕";
  } else if (isWarning) {
    bgClass = "bg-amber-800 border-amber-300 text-white";
    icon = "⚠";
  }

  toast.className = `pointer-events-auto transform transition-all duration-300 ease-out translate-y-4 opacity-0 flex items-start gap-3 p-4 rounded-2xl shadow-2xl border-l-4 ${bgClass}`;
  toast.setAttribute("role", "alert");
  toast.innerHTML = `
    <span class="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5">${icon}</span>
    <div class="toast-text flex-1 text-xs sm:text-sm font-medium leading-relaxed"></div>
    <button type="button" class="text-white/70 hover:text-white text-base leading-none p-1 -mr-1 -mt-1 font-bold focus:outline-none" aria-label="Dismiss">&times;</button>
  `;

  const textEl = toast.querySelector(".toast-text");
  if (textEl) {
    textEl.textContent = message;
  }

  const closeBtn = toast.querySelector("button");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      toast.classList.add("opacity-0", "translate-y-4");
      setTimeout(() => toast.remove(), 300);
    });
  }

  container.appendChild(toast);

  // Trigger entrance transition
  requestAnimationFrame(() => {
    toast.classList.remove("translate-y-4", "opacity-0");
    toast.classList.add("translate-y-0", "opacity-100");
  });

  // Auto dismiss after 5 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.classList.add("opacity-0", "translate-y-4");
      setTimeout(() => toast.remove(), 300);
    }
  }, 5000);
};

document.addEventListener("DOMContentLoaded", function () {
  // Auto-trigger floating toast for any server-rendered Django messages
  document.querySelectorAll("[data-django-message]").forEach(function (el) {
    const text = el.getAttribute("data-django-message");
    const tag = el.getAttribute("data-django-tag") || "info";
    if (text && typeof window.showToast === "function") {
      window.showToast(text, tag);
    }
  });
  // 1. Keyboard Navigation for Lightbox & Modals
  document.addEventListener("keydown", function (e) {
    const lb = document.getElementById("lightbox-modal");
    if (lb && !lb.classList.contains("hidden")) {
      if (e.key === "Escape") window.closeLightbox();
      if (e.key === "ArrowLeft") window.stepLightbox(-1);
      if (e.key === "ArrowRight") window.stepLightbox(1);
    }
    const gm = document.getElementById("generic-modal");
    if (gm && !gm.classList.contains("hidden")) {
      if (e.key === "Escape") window.closeGenericModal();
    }
  });

  // 2. Multi-Image Upload Previews Before Submission
  const fileInput = document.querySelector('input[type="file"][multiple]');
  const previewContainer = document.getElementById("upload-preview-container");
  if (fileInput && previewContainer) {
    fileInput.addEventListener("change", function () {
      previewContainer.innerHTML = "";
      const files = Array.from(fileInput.files || []);
      files.forEach((file) => {
        const card = document.createElement("div");
        card.className = "flex items-center gap-3 p-3 bg-[#FAF7F0] border border-[#E6DEC8] rounded-xl";
        const img = document.createElement("img");
        img.className = "w-16 h-16 object-cover rounded-lg border";
        img.alt = file.name;
        const caption = document.createElement("div");
        caption.className = "text-xs text-slate-700 font-medium";
        const sizeKB = Math.round(file.size / 1024);
        caption.textContent = `${file.name} (${sizeKB} KB)`;

        const reader = new FileReader();
        reader.onload = function (ev) {
          img.src = ev.target.result;
        };
        reader.readAsDataURL(file);

        card.appendChild(img);
        card.appendChild(caption);
        previewContainer.appendChild(card);
      });
    });
  }
});
