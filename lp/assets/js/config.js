/**
 * LP の URL 設定（URL 類はこのファイルで一元管理する）
 *
 * HTML 側は data-href="store.ios" のようにキーを指定するだけでよい。
 * ※ OGP / Twitter カードの URL はクローラーが JS を実行しないため
 *   index.html の <head> に直接記載している。変更時はそちらも合わせて更新すること。
 */
window.LP_CONFIG = {
  store: {
    ios: "https://apps.apple.com/jp/app/id0000000000", // 仮
    android: "https://play.google.com/store/apps/details?id=com.example.samplepuzzle", // 仮
  },
  sns: {
    x: "https://x.com/example_sample_puzzle", // 仮
  },
  footer: {
    terms: "https://example.com/terms", // 仮
    privacy: "https://example.com/privacy", // 仮
    contact: "https://example.com/contact", // 仮
  },
};
