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

  /* ---------- C01 追従 CTA バー ----------
   * 状態A: S02 が画面内 → 非表示
   * 状態B: S02 が画面より上に抜けた → 表示
   * 状態C: フッター到達時も表示継続（末尾の余白は CSS 側で確保）
   */
  var cta = document.getElementById("s02");
  var bar = document.getElementById("c01");

  function setBarVisible(visible) {
    bar.classList.toggle("is-visible", visible);
    bar.setAttribute("aria-hidden", visible ? "false" : "true");
    bar.querySelectorAll("a").forEach(function (a) {
      a.tabIndex = visible ? 0 : -1;
    });
  }

  if (cta && bar) {
    setBarVisible(false);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        var e = entries[0];
        // 画面下にある（まだ到達していない）間は出さない。上に抜けたら出す。
        setBarVisible(!e.isIntersecting && e.boundingClientRect.top < 0);
      }).observe(cta);
    } else {
      var onScroll = function () {
        setBarVisible(cta.getBoundingClientRect().bottom < 0);
      };
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    }
  }

  /* ---------- スライダー（S04 / S05）: 左右矢印 + ドット + スワイプ ---------- */
  document.querySelectorAll("[data-slider]").forEach(function (slider) {
    var track = slider.querySelector(".slider__track");
    var slides = Array.prototype.slice.call(track.children);
    var dotsWrap = slider.querySelector(".slider__dots");
    var label = slider.getAttribute("aria-label") || "";
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
    }

    function goTo(index) {
      var n = slides.length;
      index = (index + n) % n; // 端ではループ
      var slide = slides[index];
      track.scrollTo({
        left: slide.offsetLeft - (track.clientWidth - slide.clientWidth) / 2,
        behavior: "smooth",
      });
      render(index);
    }

    // スワイプ（ネイティブスクロール + scroll-snap）後に現在位置を同期
    var timer;
    track.addEventListener(
      "scroll",
      function () {
        clearTimeout(timer);
        timer = setTimeout(function () {
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
          if (nearest !== current) render(nearest);
        }, 80);
      },
      { passive: true }
    );

    slider.querySelector(".slider__arrow--prev").addEventListener("click", function () {
      goTo(current - 1);
    });
    slider.querySelector(".slider__arrow--next").addEventListener("click", function () {
      goTo(current + 1);
    });

    render(0);
  });
})();
