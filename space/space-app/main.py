import streamlit as st
import random

# Game setup
SCREEN_WIDTH = 800
player_width = 64
alien_width = 64
alien_height = 64

# Session state initialization
if "player_x" not in st.session_state:
    st.session_state.player_x = SCREEN_WIDTH // 2
if "bullets" not in st.session_state:
    st.session_state.bullets = []
if "aliens" not in st.session_state:
    st.session_state.aliens = [{"x": random.randint(0, SCREEN_WIDTH - alien_width), "y": 0} for _ in range(5)]
if "score" not in st.session_state:
    st.session_state.score = 0
if "lives" not in st.session_state:
    st.session_state.lives = 3
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🛸 Space Invaders (Streamlit Version)")

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Move Left"):
        st.session_state.player_x = max(0, st.session_state.player_x - 50)
with col2:
    if st.button("🔫 Shoot"):
        st.session_state.bullets.append({"x": st.session_state.player_x + player_width // 2, "y": 550})
with col3:
    if st.button("➡️ Move Right"):
        st.session_state.player_x = min(SCREEN_WIDTH - player_width, st.session_state.player_x + 50)

# Update bullets
new_bullets = []
for bullet in st.session_state.bullets:
    bullet["y"] -= 50
    if bullet["y"] > 0:
        new_bullets.append(bullet)
st.session_state.bullets = new_bullets

# Update aliens
new_aliens = []
for alien in st.session_state.aliens:
    alien["y"] += 30
    # Collision with player
    if abs(alien["x"] - st.session_state.player_x) < alien_width and alien["y"] > 500:
        st.session_state.lives -= 1
        if st.session_state.lives == 0:
            st.session_state.game_over = True
        continue
    new_aliens.append(alien)
st.session_state.aliens = new_aliens

# Collision detection
remaining_bullets = []
for bullet in st.session_state.bullets:
    hit = False
    for alien in st.session_state.aliens:
        if abs(bullet["x"] - alien["x"]) < 40 and abs(bullet["y"] - alien["y"]) < 40:
            st.session_state.score += 10
            st.session_state.aliens.remove(alien)
            hit = True
            break
    if not hit:
        remaining_bullets.append(bullet)
st.session_state.bullets = remaining_bullets

# Respawn aliens if needed
while len(st.session_state.aliens) < 5:
    st.session_state.aliens.append({"x": random.randint(0, SCREEN_WIDTH - alien_width), "y": 0})

# Display
st.markdown("---")
st.write(f"**Player X Position:** {st.session_state.player_x}")
st.write(f"**Score:** {st.session_state.score}")
st.write(f"**Lives:** {st.session_state.lives}")
st.write(f"**Aliens on Screen:** {len(st.session_state.aliens)}")
st.write(f"**Bullets Active:** {len(st.session_state.bullets)}")

if st.session_state.game_over:
    st.error("💀 GAME OVER! Please refresh the page to restart.")

