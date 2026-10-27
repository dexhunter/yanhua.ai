/* Subscription delivery. The email form lives only in the
   bottom-right dialog. subscribe.yanhua.ai is the Cloudflare Worker
   in front of Resend audience 0f2fbb4e-3333-43c1-a0d2-16c69a7c3003.
   The browser posts {email, lang, source} and reads
   {"ok":true,"subscribers":N} from statsEndpoint. RESEND_API_KEY
   stays on the worker. */
window.YANHUA_CONFIG = {
  siteUrl: "https://yanhua.ai",
  subscribeEndpoint: "https://subscribe.yanhua.ai",
  statsEndpoint: "https://subscribe.yanhua.ai/stats",
  resendAudienceId: "0f2fbb4e-3333-43c1-a0d2-16c69a7c3003",
  subscribeMethod: "POST",
  /* "json" sends {email, lang, source}. "form" sends URL-encoded fields
     (use this for Formspree). */
  subscribeFormat: "json",
  subscribeHeaders: {},
  extraFields: {},
  mailto: "",
  githubIssueUrl: "https://github.com/dexhunter/yanhua.ai/issues/new",
  substackUrl: "",
  /* Optional external analytics. Leave blank to keep the built-in
     visitor and subscriber counter only.
     cloudflareBeaconToken: Cloudflare Web Analytics token.
     goatcounterCode: the site code, "yanhua" or "yanhua.goatcounter.com".
     plausibleDomain: the domain registered in Plausible, "yanhua.ai". */
  cloudflareBeaconToken: "",
  goatcounterCode: "",
  plausibleDomain: ""
};
