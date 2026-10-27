/* Subscription delivery. Leave subscribeEndpoint empty to use the
   on-device confirmation plus the GitHub Issue / mailto fallback.
   Set an endpoint to POST subscriptions to Buttondown, Loops,
   Formspree, or a Cloudflare Worker. The form still confirms locally
   if the network request fails. */
window.YANHUA_CONFIG = {
  siteUrl: "https://yanhua.ai",
  subscribeEndpoint: "",
  subscribeMethod: "POST",
  /* "json" sends {email, lang, source}. "form" sends URL-encoded fields
     (use this for Formspree). */
  subscribeFormat: "json",
  subscribeHeaders: {},
  extraFields: {},
  mailto: "",
  githubIssueUrl: "https://github.com/dexhunter/yanhua.ai/issues/new",
  substackUrl: ""
};
