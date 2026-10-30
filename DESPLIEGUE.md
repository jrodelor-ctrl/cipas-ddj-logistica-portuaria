# Publicar el dashboard de CIPAS DDJ

**Opción recomendada: Streamlit Community Cloud.**

1. Suba el contenido de la carpeta CIPAS_DDJ_Puerto a un repositorio GitHub (sin subir `.venv`, secretos o datos privados).
2. Entre a https://share.streamlit.io/ y conecte su cuenta GitHub.
3. Seleccione **Create app**, el repositorio, la rama `main` y como archivo de inicio `app.py`.
4. Confirme que `requirements.txt` está en la raíz y publique la aplicación.
5. Abra el enlace `*.streamlit.app` desde Android, Windows u otro dispositivo con navegador e Internet.

## Consideraciones
- Esta demostración incluye datos académicos simulados. Si se incorporan registros reales, verifique privacidad, autorización y acceso público.
- El entorno del servidor no conserva indefinidamente cambios derivados de archivos subidos por visitantes; no existe base de datos permanente.
- Los botones del marco interno de Streamlit, por ejemplo el del explorador de archivos y opciones del gráfico, pueden permanecer en inglés según versión/idioma; los controles creados por nuestra aplicación están en español.
- Para probar en la red local, ejecute `python -m streamlit run app.py --server.address 0.0.0.0` y abra `http://IP_LOCAL_DEL_PC:8501` desde un equipo en la misma Wi-Fi (si el firewall lo permite). No exponga el puerto directamente a Internet.
