import pandas as pd
import streamlit as st
import altair as alt
import zipfile

st.set_page_config(page_title="Dashboard de ventas", layout="wide")

st.markdown("""
<style>
.banner {
    padding: 1.6rem 1.8rem;
    border-radius: 16px;
    background: linear-gradient(120deg, #0f172a, #1e293b, #020617);
    color: #f8fafc;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.45);
    position: relative;
    overflow: hidden;
}

.banner::after {
    content: "";
    position: absolute;
    top: -40%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(56,189,248,0.18), transparent 70%);
}

.banner-chip {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    border-radius: 999px;
    background: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    margin-bottom: 0.6rem;
}

.banner-title {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 0.3rem;
}

.banner-subtitle {
    font-size: 1rem;
    opacity: 0.85;
    margin-bottom: 0.8rem;
}

.banner-footer {
    font-size: 0.85rem;
    opacity: 0.75;
}
</style>

<div class="banner">
    <div class="banner-chip">PROYECTO FINAL · STREAMLIT</div>
    <div class="banner-title">Visualización de Datos</div>
    <div class="banner-subtitle">
        Dashboard interactivo de ventas
    </div>
    <div class="banner-footer">
        Álvaro Bilbao Pardo
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

alt.themes.enable("default")

def chart_style():
    return {
        "config": {
            "view": {"stroke": None},
            "axis": {
                "grid": True,
                "labelFontSize": 12,
                "titleFontSize": 13,
                "ticks": False,
                "domain": False
            },
            "legend": {"labelFontSize": 12, "titleFontSize": 12},
        }
    }

alt.themes.register("clean_theme", chart_style)
alt.themes.enable("clean_theme")

COLOR_VENTAS = "#1f77b4"
COLOR_PROMO = "#ff7f0e"
COLOR_TRANS = "#2ca02c"
COLOR_FEST = "#9467bd"
COLOR_ESTADO = "#17becf"
COLOR_REF = "#444444"

def cargar_datos():
    with zipfile.ZipFile("parte_1.csv.zip", "r") as z1:
        n1 = [n for n in z1.namelist() if n.endswith(".csv") and "__MACOSX" not in n][0]
        df1 = pd.read_csv(z1.open(n1), parse_dates=["date"])

    with zipfile.ZipFile("parte_2.csv.zip", "r") as z2:
        n2 = [n for n in z2.namelist() if n.endswith(".csv") and "__MACOSX" not in n][0]
        df2 = pd.read_csv(z2.open(n2), parse_dates=["date"])

    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = cargar_datos()

df["sales"] = df["sales"].fillna(0)
df["transactions"] = df["transactions"].fillna(0)
df["onpromotion"] = df["onpromotion"].fillna(0)

df["day_of_week"] = df["day_of_week"].astype(str).str.strip()
df["state"] = df["state"].astype(str).str.strip()
df["family"] = df["family"].astype(str).str.strip()

with st.expander("Información acerca del dataset analizado"):
    st.write("Número de filas totales:", df.shape[0])
    st.write("Numero de tiendas únicas:", df["store_nbr"].nunique())
    st.write("Número de productos únicos:", df["family"].nunique())
    st.write("Estados:", df["state"].nunique())
    st.write("Años:", sorted(df["year"].unique()))

st.title("Dashboard de Ventas")

tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "Página de inicio",
    "(P1) Visión global",
    "(P2) Análisis por tienda",
    "(P3) Análisis por estado",
    "(P4) Insights avanzados"
])

with tab0:
    st.header("Índice del dashboard")

    st.markdown("""
    Este dashboard está organizado en pestañas que facilitan la búsqueda y organización de la información
    desde una visión más global, a información más específica
    """)

    st.divider()

    st.markdown("""
    ### Visión global
    Esta pestaña contiene:
    - Indicadores clave (tiendas, productos, estados, meses)
    - Rankings de productos, tiendas y promociones
    - Análisis de estacionalidad por día, semana del año y mes
    """)

    st.markdown("""
    ### Análisis por tienda
    Esta pestaña contiene:
    - Evolución anual de ventas
    - Volumen total de productos vendidos
    - Impacto de las promociones en cada tienda
    """)

    st.markdown("""
    ### Análisis por estado
    Esta pestaña contiene:
    - Evolución de transacciones a lo largo del tiempo
    - Ranking de tiendas con mayor volumen de ventas
    - Identificación del producto líder en la tienda (por defecto, la líder del estado)
    """)

    st.markdown("""
    ### Información avanzada
    Esta pestaña contiene:
    - Impacto y eficiencia de las promociones
    - Ticket medio y evolución temporal
    - Efecto de festivos y concentración de ventas
    """)

    st.divider()

    st.caption(
        "*Esta pestaña no se menciona en el enunciado pero se ha querido añadir a modo de portada con índice para lograr"
        " un resultado más profesional y completo"
    )

with tab1:
    st.header("Indicadores clave")

    col1, col2, col3, col4 = st.columns(4)
    meses_disponibles = df["date"].dt.to_period("M").nunique()

    col1.metric("Tiendas", df["store_nbr"].nunique())
    col2.metric("Productos", df["family"].nunique())
    col3.metric("Estados", df["state"].nunique())
    col4.metric("Meses", meses_disponibles)

    st.markdown("**Escoger una métrica de análisis (Media de ventas/Ventas totales) para el apartado 1.b:**")
    tipo_analisis = st.radio(
        "",
        ["Media de ventas", "Ventas totales"],
        horizontal=True,
        index=0
    )
    st.caption(
        "La vista por «media» cumple el análisis en términos medios solicitado en el enunciado. "
        "La vista por «total», por otro lado, se incluye como apoyo por si se quiere interpretar a nivel de volumen."
    )

    st.subheader("Ranking (Top 10) de productos más vendidos")

    if tipo_analisis == "Media de ventas":
        top_productos = (
            df.groupby("family", as_index=False)["sales"]
            .mean()
            .sort_values("sales", ascending=False)
            .head(10)
        )
        y_title = "Ventas medias"
    else:
        top_productos = (
            df.groupby("family", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
            .head(10)
        )
        y_title = "Ventas totales"

    chart_top_prod = (
        alt.Chart(top_productos)
        .mark_bar(color=COLOR_VENTAS)
        .encode(
            x=alt.X("sales:Q", title=y_title),
            y=alt.Y("family:N", sort="-x", title=None),
            tooltip=[
                alt.Tooltip("family:N", title="Producto"),
                alt.Tooltip("sales:Q", title=y_title, format=",.2f")
            ]
        )
        .properties(height=320)
    )
    st.altair_chart(chart_top_prod, use_container_width=True)

    st.divider()

    st.subheader("Distribución de ventas por tienda")

    if tipo_analisis == "Media de ventas":
        ventas_tienda = (
            df.groupby("store_nbr", as_index=False)["sales"]
            .mean()
            .sort_values("sales", ascending=False)
        )
        y_title = "Ventas medias"
    else:
        ventas_tienda = (
            df.groupby("store_nbr", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
        )
        y_title = "Ventas totales"

    ventas_tienda_plot = ventas_tienda.copy()

    chart_tienda = (
        alt.Chart(ventas_tienda_plot)
        .mark_bar(color=COLOR_VENTAS)
        .encode(
            x=alt.X("store_nbr:O", title="Tienda"),
            y=alt.Y("sales:Q", title=y_title),
            tooltip=[
                alt.Tooltip("store_nbr:O", title="Tienda"),
                alt.Tooltip("sales:Q", title=y_title, format=",.2f")
            ]
        )
        .properties(height=320)
    )
    st.altair_chart(chart_tienda, use_container_width=True)

    st.subheader("Distribución (histograma) de ventas por tienda")

    hist_df = ventas_tienda[["sales"]].copy()

    chart_hist = (
        alt.Chart(hist_df)
        .mark_bar(color=COLOR_VENTAS)
        .encode(
            x=alt.X("sales:Q", bin=alt.Bin(maxbins=30), title=y_title),
            y=alt.Y("count():Q", title="Número de tiendas"),
            tooltip=[
                alt.Tooltip("count():Q", title="Tiendas"),
                alt.Tooltip("sales:Q", bin=True, title=y_title)
            ]
        )
        .properties(height=280)
    )

    st.altair_chart(chart_hist, use_container_width=True)
    st.caption(
        "El gráfico superior compara tiendas. "
        "El histograma inferior representa la distribución estadística de ventas por tienda."
    )

    st.divider()

    st.subheader("Ranking (Top 10) de tiendas con ventas en promoción")

    df_promo = df[df["onpromotion"] > 0]

    if tipo_analisis == "Media de ventas":
        promo_tiendas = (
            df_promo.groupby("store_nbr", as_index=False)["sales"]
            .mean()
            .sort_values("sales", ascending=False)
            .head(10)
        )
        y_title = "Ventas medias (promo)"
    else:
        promo_tiendas = (
            df_promo.groupby("store_nbr", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
            .head(10)
        )
        y_title = "Ventas totales (promo)"

    chart_promo_tienda = (
        alt.Chart(promo_tiendas)
        .mark_bar(color=COLOR_PROMO)
        .encode(
            x=alt.X("sales:Q", title=y_title),
            y=alt.Y("store_nbr:O", sort="-x", title=None),
            tooltip=[
                alt.Tooltip("store_nbr:O", title="Tienda"),
                alt.Tooltip("sales:Q", title=y_title, format=",.2f")
            ]
        )
        .properties(height=280)
    )
    st.altair_chart(chart_promo_tienda, use_container_width=True)

    st.divider()

    st.subheader("Estacionalidad de las ventas")

    orden_dias_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    orden_dias_es = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dias_presentes = set(df["day_of_week"].dropna().unique())
    if set(orden_dias_es).issubset(dias_presentes):
        orden_dias = orden_dias_es
    else:
        orden_dias = orden_dias_en

    ventas_dia_df = (
        df.groupby("day_of_week", as_index=False)["sales"]
        .mean()
    )
    media_global = ventas_dia_df["sales"].mean()

    bars = (
        alt.Chart(ventas_dia_df)
        .mark_bar(color=COLOR_VENTAS)
        .encode(
            x=alt.X("day_of_week:N", sort=orden_dias, title="Día de la semana"),
            y=alt.Y("sales:Q", title="Ventas medias"),
            tooltip=[
                alt.Tooltip("day_of_week:N", title="Día"),
                alt.Tooltip("sales:Q", title="Ventas medias", format=",.2f")
            ]
        )
    )
    ref_line = (
        alt.Chart(pd.DataFrame({"media_global": [media_global]}))
        .mark_rule(strokeDash=[6, 6], color=COLOR_REF)
        .encode(y="media_global:Q")
    )
    chart_dias = (bars + ref_line).properties(height=300)
    st.altair_chart(chart_dias, use_container_width=True)
    st.caption("La línea discontinua representa la media global de ventas.")

    st.divider()

    st.subheader("Volumen de ventas medio por semana del año")

    ventas_semana = (
        df.groupby("week", as_index=False)["sales"]
        .mean()
        .sort_values("week")
    )
    chart_semana = (
        alt.Chart(ventas_semana)
        .mark_line(point=True, color=COLOR_VENTAS)
        .encode(
            x=alt.X("week:O", title="Semana del año"),
            y=alt.Y("sales:Q", title="Ventas medias"),
            tooltip=[
                alt.Tooltip("week:O", title="Semana"),
                alt.Tooltip("sales:Q", title="Ventas medias", format=",.2f")
            ]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_semana, use_container_width=True)

    st.divider()

    st.subheader("Volumen de ventas medio por mes")

    ventas_mes = (
        df.groupby("month", as_index=False)["sales"]
        .mean()
        .sort_values("month")
    )
    chart_mes = (
        alt.Chart(ventas_mes)
        .mark_line(point=True, color=COLOR_VENTAS)
        .encode(
            x=alt.X("month:O", title="Mes"),
            y=alt.Y("sales:Q", title="Ventas medias"),
            tooltip=[
                alt.Tooltip("month:O", title="Mes"),
                alt.Tooltip("sales:Q", title="Ventas medias", format=",.2f")
            ]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_mes, use_container_width=True)

with tab2:
    st.header("Análisis por Tienda")

    tienda_seleccionada = st.selectbox(
        "Selecciona una tienda del desplegable:",
        sorted(df["store_nbr"].unique())
    )

    df_tienda = df[df["store_nbr"] == tienda_seleccionada]

    st.subheader("Número total de ventas por año (de más antiguo a más reciente)")
    ventas_anuales = (
        df_tienda.groupby("year", as_index=False)["sales"]
        .sum()
        .sort_values("year")
    )

    chart_ventas_anual = (
        alt.Chart(ventas_anuales)
        .mark_bar(color=COLOR_VENTAS)
        .encode(
            x=alt.X("year:O", title="Año"),
            y=alt.Y("sales:Q", title="Ventas totales"),
            tooltip=[
                alt.Tooltip("year:O", title="Año"),
                alt.Tooltip("sales:Q", title="Ventas", format=",.0f")
            ]
        )
        .properties(height=320)
    )
    st.altair_chart(chart_ventas_anual, use_container_width=True)

    st.divider()

    st.subheader("Número total de productos vendidos")
    total_productos = int(round(df_tienda["sales"].sum()))
    productos_promo = int(round(df_tienda[df_tienda["onpromotion"] > 0]["sales"].sum()))

    c1, c2 = st.columns(2)
    c1.metric("Unidades vendidas", f"{total_productos:,}")
    c2.metric("Unidades en promoción", f"{productos_promo:,}")

    st.subheader("Evolución mensual de ventas")

    df_tienda_tmp = df_tienda.copy()
    df_tienda_tmp["ym"] = df_tienda_tmp["date"].dt.to_period("M").astype(str)

    tienda_mensual = (
        df_tienda_tmp.groupby("ym", as_index=False)["sales"]
        .sum()
    )

    chart_tienda_mensual = (
        alt.Chart(tienda_mensual)
        .mark_line(point=True, color=COLOR_VENTAS)
        .encode(
            x=alt.X("ym:N", title="Mes"),
            y=alt.Y("sales:Q", title="Ventas totales"),
            tooltip=[
                alt.Tooltip("ym:N", title="Mes"),
                alt.Tooltip("sales:Q", title="Ventas", format=",.0f")
            ]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_tienda_mensual, use_container_width=True)
    st.caption("Gráfico adicional para contextualizar la tendencia de la tienda.")

with tab3:
    st.header("Análisis por estado")

    estado_seleccionado = st.selectbox(
        "Selecciona un estado del desplegable:",
        sorted(df["state"].dropna().unique())
    )

    df_estado = df[df["state"] == estado_seleccionado]

    st.subheader("Número total de transacciones por año")
    transacciones_anuales = (
        df_estado.groupby("year", as_index=False)["transactions"]
        .sum()
        .sort_values("year")
    )

    chart_trans = (
        alt.Chart(transacciones_anuales)
        .mark_bar(color=COLOR_TRANS)
        .encode(
            x=alt.X("year:O", title="Año"),
            y=alt.Y("transactions:Q", title="Transacciones totales"),
            tooltip=[
                alt.Tooltip("year:O", title="Año"),
                alt.Tooltip("transactions:Q", title="Transacciones", format=",.0f")
            ]
        )
        .properties(height=320)
    )
    st.altair_chart(chart_trans, use_container_width=True)

    st.divider()

    n_tiendas_estado = df_estado["store_nbr"].nunique()
    st.subheader(f"Ranking de tiendas con más ventas (Top {min(10, n_tiendas_estado)})")

    ranking_tiendas = (
        df_estado.groupby("store_nbr", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .head(10)
    )

    chart_rank = (
        alt.Chart(ranking_tiendas)
        .mark_bar(color=COLOR_VENTAS)
        .encode(
            x=alt.X("sales:Q", title="Ventas totales"),
            y=alt.Y("store_nbr:O", sort="-x", title=None),
            tooltip=[
                alt.Tooltip("store_nbr:O", title="Tienda"),
                alt.Tooltip("sales:Q", title="Ventas", format=",.0f")
            ]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_rank, use_container_width=True)

    st.divider()

    st.subheader("Producto más vendido en la tienda")

    ventas_por_tienda_estado = (
        df_estado.groupby("store_nbr")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    if ventas_por_tienda_estado.empty:
        st.warning("No hay datos de ventas para este estado.")
    else:
        tienda_lider = ventas_por_tienda_estado.index[0]
        tiendas_estado = sorted(df_estado["store_nbr"].unique())

        tienda_seleccionada_estado = st.selectbox(
            "Selecciona una tienda dentro del estado:",
            options=tiendas_estado,
            index=tiendas_estado.index(tienda_lider)
        )

        df_estado_tienda = df_estado[df_estado["store_nbr"] == tienda_seleccionada_estado]

        producto_top = (
            df_estado_tienda.groupby("family")["sales"]
            .sum()
            .sort_values(ascending=False)
            .idxmax()
        )

        c1, c2 = st.columns(2)
        c1.metric("Tienda seleccionada", int(tienda_seleccionada_estado))
        c2.metric("Producto más vendido", producto_top)

        st.subheader("Top 10 productos en la tienda seleccionada")

        top10_prod_tienda = (
            df_estado_tienda.groupby("family", as_index=False)["sales"]
            .sum()
            .sort_values("sales", ascending=False)
            .head(10)
        )

        chart_prod_tienda = (
            alt.Chart(top10_prod_tienda)
            .mark_bar(color=COLOR_PROMO)
            .encode(
                x=alt.X("sales:Q", title="Ventas totales"),
                y=alt.Y("family:N", sort="-x", title=None),
                tooltip=[
                    alt.Tooltip("family:N", title="Producto"),
                    alt.Tooltip("sales:Q", title="Ventas", format=",.0f")
                ]
            )
            .properties(height=320)
        )

        st.altair_chart(chart_prod_tienda, use_container_width=True)
        st.caption(
            "Por defecto se muestra la tienda líder del estado, pero se puede seleccionar "
            "cualquier otra tienda para analizar su producto más vendido."
        )
        st.caption("Gráfico adicional para visualizar el Top 10 de productos dentro de la tienda seleccionada.")

with tab4:
    st.header("Información avanzada")
    st.info("Análisis adicional para ayudar en la toma de decisiones y conclusiones")

    st.subheader("Resumen")

    ventas_dia = df.groupby("day_of_week")["sales"].mean()
    mejor_dia = ventas_dia.idxmax()

    ventas_mes = df.groupby("month")["sales"].mean()
    mejor_mes = int(ventas_mes.idxmax())

    ventas_estado = df.groupby("state")["sales"].sum().sort_values(ascending=False)
    estado_top = ventas_estado.index[0]
    pct_estado_top = ventas_estado.iloc[0] / ventas_estado.sum() * 100 if ventas_estado.sum() != 0 else 0

    df_tmp = df.copy()
    df_tmp["promo"] = df_tmp["onpromotion"] > 0
    ventas_total = df_tmp["sales"].sum()
    ventas_promo_total = df_tmp[df_tmp["promo"]]["sales"].sum()
    share_promo = ventas_promo_total / ventas_total * 100 if ventas_total != 0 else 0

    total_trans = df["transactions"].sum()
    ticket_global = df["sales"].sum() / total_trans if total_trans != 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Mejor día (media)", str(mejor_dia))
    c2.metric("Mejor mes (media)", str(mejor_mes))
    c3.metric("Mejor estado", f"{estado_top}")
    c4.metric("Mejor % ventas del estado", f"{pct_estado_top:,.1f}%")
    c5.metric("Ventas en promoción", f"{share_promo:,.1f}%")

    st.caption(
        f"- El mejor día por ventas medias es **{mejor_dia}** y el mejor mes es **{mejor_mes}**. \n"
        f"- El estado con mayor contribución es **{estado_top}** ({pct_estado_top:,.1f}% del total).  \n"
        f"- Las ventas en promoción representan **{share_promo:,.1f}%** del total.  \n"
    )

    st.divider()

    st.subheader("Impacto, contribución y dónde funcionan mejor las promociones")

    media_promo = df_tmp[df_tmp["promo"]]["sales"].mean()
    media_no = df_tmp[~df_tmp["promo"]]["sales"].mean()
    lift = (media_promo / media_no) - 1 if media_no != 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Media ventas con promoción", f"{media_promo:,.2f}")
    c2.metric("Media ventas sin promoción", f"{media_no:,.2f}")
    c3.metric("Lift de la promoción", f"{lift*100:,.1f}%")
    c4.metric("Ventas en promoción / total", f"{share_promo:,.1f}%")

    promo_vs_no = (
        df_tmp.groupby("promo", as_index=False)["sales"]
        .mean()
        .rename(columns={"sales": "ventas_medias"})
    )
    chart_promo = (
        alt.Chart(promo_vs_no)
        .mark_bar(color=COLOR_PROMO)
        .encode(
            x=alt.X("promo:N", title="¿Están en promoción?"),
            y=alt.Y("ventas_medias:Q", title="Ventas medias"),
            tooltip=[
                alt.Tooltip("promo:N", title="Promo"),
                alt.Tooltip("ventas_medias:Q", title="Ventas medias", format=",.2f")
            ]
        )
        .properties(height=260)
    )
    st.altair_chart(chart_promo, use_container_width=True)

    st.markdown("**Top 10 estados con mayor lift de promoción**")

    lift_estado = (
        df_tmp.groupby(["state", "promo"])["sales"].mean().reset_index()
        .pivot(index="state", columns="promo", values="sales")
        .rename(columns={False: "no_promo", True: "promo"})
    )
    lift_estado = lift_estado.fillna(0)
    lift_estado["lift"] = lift_estado.apply(
        lambda x: (x["promo"] / x["no_promo"]) - 1 if x["no_promo"] != 0 else 0,
        axis=1
    )
    lift_estado = lift_estado.sort_values("lift", ascending=False).head(10).reset_index()

    chart_lift_estado = (
        alt.Chart(lift_estado)
        .mark_bar(color=COLOR_VENTAS)
        .encode(
            x=alt.X("lift:Q", title="Lift con promoción vs sin promoción"),
            y=alt.Y("state:N", sort="-x", title=None),
            tooltip=[
                alt.Tooltip("state:N", title="Estado"),
                alt.Tooltip("lift:Q", title="Lift", format=",.2%")
            ]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_lift_estado, use_container_width=True)

    st.divider()

    st.subheader("Impacto en ventas (media) de los festivos")

    ventas_festivo = (
        df.groupby("holiday_type", as_index=False)["sales"]
        .mean()
        .rename(columns={"sales": "ventas_medias"})
        .sort_values("ventas_medias", ascending=False)
    )

    chart_festivo = (
        alt.Chart(ventas_festivo)
        .mark_bar(color=COLOR_FEST)
        .encode(
            x=alt.X("holiday_type:N", sort="-y", title="Tipo de festivo"),
            y=alt.Y("ventas_medias:Q", title="Ventas medias"),
            tooltip=[
                alt.Tooltip("holiday_type:N", title="Festivo"),
                alt.Tooltip("ventas_medias:Q", title="Ventas medias", format=",.2f")
            ]
        )
        .properties(height=320)
    )
    st.altair_chart(chart_festivo, use_container_width=True)
    st.caption(
        "Este gráfico permite identificar qué tipos de festivo están asociados con un mayor nivel de ventas medias."
    )

    st.divider()

    st.subheader("Crecimiento interanual")

    ventas_anio = (
        df.groupby("year", as_index=False)["sales"]
        .sum()
        .rename(columns={"sales": "ventas_totales"})
        .sort_values("year")
    )
    ventas_anio["yoy_pct"] = ventas_anio["ventas_totales"].pct_change() * 100

    c1, c2 = st.columns(2)
    if len(ventas_anio) >= 2:
        ultimo = ventas_anio.iloc[-1]
        anterior = ventas_anio.iloc[-2]
        c1.metric("Ventas último año", f"{ultimo['ventas_totales']:,.0f}")
        c2.metric(
            "Crecimiento interanual último año",
            f"{(ultimo['ventas_totales']/anterior['ventas_totales']-1)*100:,.1f}%"
        )
    else:
        c1.metric("Ventas", f"{ventas_anio['ventas_totales'].sum():,.0f}")
        c2.metric("Crecimiento interanual", "N/A")

    chart_yoy = (
        alt.Chart(ventas_anio)
        .mark_line(point=True, color=COLOR_TRANS)
        .encode(
            x=alt.X("year:O", title="Año"),
            y=alt.Y("ventas_totales:Q", title="Ventas totales"),
            tooltip=[
                alt.Tooltip("year:O", title="Año"),
                alt.Tooltip("ventas_totales:Q", title="Ventas", format=",.0f"),
                alt.Tooltip("yoy_pct:Q", title="YoY %", format=",.2f")
            ]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_yoy, use_container_width=True)

    st.divider()

    st.subheader("Concentración de ventas")

    modo_pareto = st.radio(
        "Elegir por qué analizar la concentración:",
        ["Tiendas", "Productos"],
        horizontal=True
    )

    if modo_pareto == "Tiendas":
        serie = df.groupby("store_nbr")["sales"].sum().sort_values(ascending=False)
        etiqueta = "store_nbr"
    else:
        serie = df.groupby("family")["sales"].sum().sort_values(ascending=False)
        etiqueta = "family"

    pareto = serie.reset_index()
    pareto.columns = [etiqueta, "ventas"]
    total = pareto["ventas"].sum()
    pareto["pct_acum"] = pareto["ventas"].cumsum() / total * 100 if total != 0 else 0
    pareto["rank"] = range(1, len(pareto) + 1)

    n80 = int((pareto["pct_acum"] <= 80).sum())
    st.metric(f"Nº de {modo_pareto.lower()} para llegar al 80% de ventas", n80)

    pareto_plot = pareto.head(50)
    chart_pareto = (
        alt.Chart(pareto_plot)
        .mark_line(point=True, color=COLOR_ESTADO)
        .encode(
            x=alt.X("rank:O", title=f"Ranking (Top 50) de {modo_pareto.lower()}"),
            y=alt.Y("pct_acum:Q", title="% acumulado de ventas"),
            tooltip=[
                alt.Tooltip("rank:O", title="Rank"),
                alt.Tooltip(etiqueta + ":N", title=modo_pareto[:-1]),
                alt.Tooltip("pct_acum:Q", title="% acumulado", format=",.2f")
            ]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_pareto, use_container_width=True)
    st.caption(
        "Ayuda a entender si las ventas están concentradas en pocos elementos o están más repartidas. "
        "Se utiliza la regla de Pareto (80/20). Por legibilidad se limita la visualización al Top 50."
    )
