"""Login left panel — full-height image + plane takeoff animation (iframe)."""
import html
import streamlit.components.v1 as components

LOGIN_IMAGES = {
    "mobile": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1600&q=85",
    "otp": "https://images.unsplash.com/photo-1436491865332-7a61a1099cac?w=1600&q=85",
    "profile": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1600&q=85",
}


def render_login_visual(step: str, tagline: str, step_title: str, step_num: int, hint: str, height: int = 720) -> None:
    bg = LOGIN_IMAGES.get(step, LOGIN_IMAGES["mobile"])
    tagline = html.escape(tagline)
    hint = html.escape(hint)
    step_title = html.escape(step_title)
    panel_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden;
    font-family: 'Segoe UI', system-ui, sans-serif; }}
  .panel {{
    position: relative;
    width: 100%;
    height: {height}px;
    min-height: {height}px;
    background: url('{bg}') center center / cover no-repeat;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 14px 40px rgba(0,0,0,0.28);
    animation: kenburns 16s ease-in-out infinite alternate;
  }}
  .scrim {{
    position: absolute; inset: 0;
    background: linear-gradient(120deg, rgba(30,30,30,0.72) 0%, rgba(208,74,2,0.35) 100%);
  }}
  .cloud {{
    position: absolute; font-size: 2.2rem; opacity: 0.35; color: white;
    animation: drift 24s linear infinite;
  }}
  .c1 {{ top: 10%; left: 6%; }}
  .c2 {{ top: 18%; right: 10%; animation-delay: 8s; }}
  .trail {{
    position: absolute;
    width: 120px; height: 4px;
    background: linear-gradient(90deg, transparent, rgba(255,200,120,0.9));
    transform-origin: left center;
    animation: trail 8s ease-in-out infinite;
    z-index: 3;
  }}
  .plane {{
    position: absolute;
    font-size: 4.5rem;
    line-height: 1;
    z-index: 5;
    background: linear-gradient(145deg, #fff3e0, #ffb347, #d04a02, #ff6b35);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 8px 16px rgba(208,74,2,0.8));
    animation: takeoff 8s ease-in-out infinite;
  }}
  .badge {{
    position: absolute; top: 16px; left: 16px; z-index: 6;
    background: #d04a02; color: white; padding: 8px 14px; border-radius: 999px;
    font-size: 12px; font-weight: 700;
  }}
  .copy {{
    position: absolute; left: 20px; right: 20px; bottom: 22px; z-index: 6; color: white;
    text-shadow: 0 2px 12px rgba(0,0,0,0.6);
  }}
  .copy h1 {{ margin: 0 0 6px; font-size: 2rem; font-weight: 800; }}
  .copy p {{ margin: 4px 0 0; font-size: 0.95rem; opacity: 0.92; }}
  @keyframes kenburns {{
    from {{ background-size: 100% auto; background-position: center bottom; }}
    to {{ background-size: 108% auto; background-position: center 30%; }}
  }}
  @keyframes drift {{
    from {{ transform: translateX(0); }}
    to {{ transform: translateX(40px); }}
  }}
  @keyframes takeoff {{
    0%   {{ left: 6%;  bottom: 12%; transform: rotate(-28deg) scale(0.75); }}
    45%  {{ left: 42%; bottom: 48%; transform: rotate(-12deg) scale(1); }}
    100% {{ left: 72%; bottom: 78%; transform: rotate(8deg) scale(1.08); }}
  }}
  @keyframes trail {{
    0%   {{ left: 8%;  bottom: 14%; transform: rotate(-28deg) scaleX(0.4); opacity: 0.3; }}
    45%  {{ left: 38%; bottom: 46%; transform: rotate(-12deg) scaleX(0.9); opacity: 0.85; }}
    100% {{ left: 68%; bottom: 76%; transform: rotate(8deg) scaleX(1); opacity: 0.5; }}
  }}
</style>
</head>
<body>
  <div class="panel">
    <div class="scrim"></div>
    <div class="cloud c1">☁</div>
    <div class="cloud c2">☁</div>
    <div class="trail"></div>
    <div class="plane">✈</div>
    <div class="badge">Step {step_num} of 3 · {step_title}</div>
    <div class="copy">
      <h1>TripWise</h1>
      <p>{tagline}</p>
      <p>{hint}</p>
    </div>
  </div>
</body>
</html>
"""
    components.html(panel_html, height=height + 8, scrolling=False)
