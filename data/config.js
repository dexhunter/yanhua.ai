/* Subscription delivery. The page only asks for an email in the
   bottom-right toast. Leave subscribeEndpoint empty to confirm on
   this device and offer a GitHub Issue (labeled subscribe).

   Resend cannot be called from the browser: the API key would leak,
   and Resend blocks browser CORS. Deploy scripts/cloudflare-resend-worker.js
   and set subscribeEndpoint to that worker, for example
   "https://subscribe.yanhua.ai/subscribe". The only secret is
   RESEND_API_KEY (wrangler secret / process.env). resendAudienceId
   below is the public General segment and is already the default in
   the worker and in scripts/send_newsletter_resend.py. Set the
   RESEND_AUDIENCE_ID secret only to point at a different segment.
   Resend renamed Audiences to Segments; both still fall back to
   /audiences/:id/contacts if the segment call is rejected.

   Mail sends as "演化日报 · Yanhua Daily <digest@yanhua.ai>" once
   yanhua.ai (domain de1ea356-1c37-419f-bffa-be649f64b080) is verified.
   Before that, the worker and the sender fall back to
   onboarding@resend.dev.

   Buttondown, Loops, or Formspree also work as subscribeEndpoint.
   The form still confirms locally if the network request fails. */
window.YANHUA_CONFIG = {
  siteUrl: "https://yanhua.ai",
  subscribeEndpoint: "",
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
