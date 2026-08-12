/* 日本語 / English の切り替え。
 *
 * 初期表示の決定は各ページの <head> にあるインラインスクリプトが行う(描画前に確定させて
 * ちらつきを防ぐため)。このファイルは切り替えボタンの配線を担当する。
 *
 * JavaScript が無効な環境では html に .js が付かず、CSS の既定どおり日英の両方が表示される。
 */
(function () {
  "use strict";

  var STORAGE_KEY = "swlang";
  var root = document.documentElement;

  function buttons() {
    return document.querySelectorAll("[data-set-lang]");
  }

  function apply(lang, persist) {
    root.setAttribute("data-active-lang", lang);
    root.setAttribute("lang", lang);

    var btns = buttons();
    for (var i = 0; i < btns.length; i++) {
      var pressed = btns[i].getAttribute("data-set-lang") === lang;
      btns[i].setAttribute("aria-pressed", pressed ? "true" : "false");
    }

    if (!persist) {
      return;
    }

    try {
      window.localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* プライベートブラウズなどで保存できなくても、表示の切り替えは行う。 */
    }

    /* URL の ?lang= も合わせておく。この状態のままリンクを共有できる。 */
    try {
      var url = new URL(window.location.href);
      url.searchParams.set("lang", lang);
      window.history.replaceState(null, "", url);
    } catch (e) {
      /* 古い環境では URL を書き換えないだけで、表示には影響しない。 */
    }
  }

  function init() {
    var btns = buttons();
    for (var i = 0; i < btns.length; i++) {
      btns[i].addEventListener("click", function () {
        apply(this.getAttribute("data-set-lang"), true);
      });
    }

    /* head のインラインスクリプトが決めた言語に aria-pressed を合わせる。
       ?lang= で開かれたときは明示的な指定とみなして保存する(そのまま別のページへ
       移っても言語が保たれる)。端末の言語から自動で決まった場合は保存しない
       ── 保存すると、あとで端末の言語設定を変えても追随しなくなるため。 */
    var fromUrl = /[?&]lang=(ja|en)(?:&|$)/.test(window.location.search);
    apply(root.getAttribute("data-active-lang") === "en" ? "en" : "ja", fromUrl);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
