// utilidades simples
export const qs = (o={}) =>
  Object.entries(o).map(([k,v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join("&");

export const confirmAction = (msg="Tem certeza?") => window.confirm(msg);

export const keepParams = (...keys) => {
  const u = new URL(window.location);
  const out = {};
  keys.forEach(k => { const v = u.searchParams.get(k); if (v!==null) out[k]=v; });
  return out;
};
