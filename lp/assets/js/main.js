(function () {
  "use strict";

  var config = window.LP_CONFIG || {};

  /* ---------- 外部リンク: config.js の URL を反映（新規タブ + noopener noreferrer） ---------- */
  function lookup(path) {
    return path.split(".").reduce(function (obj, key) {
      return obj && obj[key];
    }, config);
  }

  document.querySelectorAll("[data-href]").forEach(function (a) {
    var url = lookup(a.getAttribute("data-href"));
    if (!url) return;
    a.href = url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
  });

  /* ---------- スライダー（S04 / S05）: 左右矢印 + ドット + スワイプ ---------- */
  document.querySelectorAll("[data-slider]").forEach(function (slider) {
    var track = slider.querySelector(".slider__track");
    var slides = Array.prototype.slice.call(track.children);
    var dotsWrap = slider.querySelector(".slider__dots");
    var label = slider.getAttribute("aria-label") || "";
    var prev = slider.querySelector(".slider__arrow--prev");
    var next = slider.querySelector(".slider__arrow--next");
    var current = 0;

    var dots = slides.map(function (_, i) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.className = "slider__dot";
      dot.setAttribute("aria-label", label + " " + (i + 1) + "枚目を表示");
      dot.addEventListener("click", function () {
        goTo(i);
      });
      dotsWrap.appendChild(dot);
      return dot;
    });

    function render(index) {
      current = index;
      dots.forEach(function (d, i) {
        d.classList.toggle("is-active", i === index);
        d.setAttribute("aria-current", i === index ? "true" : "false");
      });
      slides.forEach(function (s, i) {
        s.setAttribute("aria-hidden", i === index ? "false" : "true");
      });
      // 端ではそれ以上送れないので、矢印を半透明にして押せなくする
      prev.disabled = index === 0;
      next.disabled = index === slides.length - 1;
    }

    // 矢印・ドットで移動中の行き先。到着するまではスクロール位置で表示を上書きしない
    var target = null;
    var targetTimer;

    function nearestIndex() {
      var center = track.scrollLeft + track.clientWidth / 2;
      var nearest = 0;
      var best = Infinity;
      slides.forEach(function (s, i) {
        var dist = Math.abs(s.offsetLeft + s.clientWidth / 2 - center);
        if (dist < best) {
          best = dist;
          nearest = i;
        }
      });
      return nearest;
    }

    function goTo(index) {
      index = Math.max(0, Math.min(slides.length - 1, index));
      var slide = slides[index];
      target = index;
      clearTimeout(targetTimer);
      // scrollend 非対応ブラウザ向けの保険
      targetTimer = setTimeout(function () {
        target = null;
      }, 700);
      track.scrollTo({
        left: slide.offsetLeft - (track.clientWidth - slide.clientWidth) / 2,
        behavior: "smooth",
      });
      render(index); // 押した瞬間に矢印・ドットを切り替える
    }

    // スワイプ中も 1 フレームごとに現在位置を同期（止まるのを待たない）
    var ticking = false;
    track.addEventListener(
      "scroll",
      function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          ticking = false;
          var nearest = nearestIndex();
          if (target !== null) {
            if (nearest !== target) return;
            target = null;
          }
          if (nearest !== current) render(nearest);
        });
      },
      { passive: true }
    );

    track.addEventListener("scrollend", function () {
      target = null;
      var nearest = nearestIndex();
      if (nearest !== current) render(nearest);
    });

    // 指で触ったらユーザー操作を優先
    track.addEventListener(
      "touchstart",
      function () {
        target = null;
      },
      { passive: true }
    );

    prev.addEventListener("click", function () {
      goTo(current - 1);
    });
    next.addEventListener("click", function () {
      goTo(current + 1);
    });

    render(0);
  });
})();
