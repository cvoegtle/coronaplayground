import io

import altair as alt


def infection_chart(data):
    chart_data = []
    for i in range(len(data["day"])):
        chart_data.append({
            "day": data["day"][i],
            "infections": data["infections"][i],
            "kind": "2. Infektionen",
        })
    for i in range(len(data["day"])):
        chart_data.append({
            "day": data["day"][i],
            "infections": data["reports"][i],
            "kind": "1. Meldungen",
        })

    infection_chart = alt.Chart(alt.Data(values=chart_data)).mark_bar().encode(
        alt.X("monthdate(day):O", title="Tag"),
        alt.Y('sum(infections):Q', title='Fälle'),
        alt.Color('kind:O', title='Art'))

    average_chart = alt.Chart(data).mark_area(point={'color': 'orange'}, line={'color': 'orange'}, color='orange', opacity=0.15).encode(
        alt.X("monthdate(day):O", title="Tag"),
        alt.Y("four_day_average:Q"))

    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['day'], empty='none')

    selectors = alt.Chart(data).mark_point().encode(
        alt.X("monthdate(day)", title="Tag"),
        opacity=alt.value(0),
    ).add_selection(nearest)

    infection_points = infection_chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    infection_text = infection_chart.mark_text(align='left', dx=5, dy=5).encode(
        text=alt.condition(nearest, 'infections:Q', alt.value(' '))
    )

    average_points = average_chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    average_text = average_chart.mark_text(align='left', dx=5, dy=5).encode(
        text=alt.condition(nearest, 'four_day_average:Q', alt.value(' '))
    )

    rule = alt.Chart(data).mark_rule(color='gray').encode(
        alt.X("monthdate(day)", title="Tag"),
    ).transform_filter(nearest)

    return to_json(alt.layer(infection_chart,
                             average_chart,
                             selectors,
                             average_points,
                             average_text,
                             infection_points,
                             infection_text,
                             rule).properties(width=1050, height=400))


def reproduction_rate_chart(data):
    chart_reproduction_rate = alt.Chart(data).mark_line(point=True, color='red').encode(
        alt.X("monthdate(day):O", title="Tag"),
        alt.Y("reproduction_rate:Q", title="Reproduktionsrate"))

    reproduction_nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                         fields=['day'], empty='none')
    reproduction_selectors = alt.Chart(data).mark_point().encode(
        alt.X("monthdate(day)", title="Tag"),
        opacity=alt.value(0),
    ).add_selection(reproduction_nearest)

    reproduction_points = chart_reproduction_rate.mark_point().encode(
        opacity=alt.condition(reproduction_nearest, alt.value(1), alt.value(0))
    )

    reproduction_text = chart_reproduction_rate.mark_text(align='left', dx=5, dy=5).encode(
        text=alt.condition(reproduction_nearest, 'reproduction_rate:Q', alt.value(' '))
    )

    rule = alt.Chart(data).mark_rule(color='gray').encode(
        alt.X("monthdate(day)", title="Tag"),
    ).transform_filter(reproduction_nearest)

    combinded_chart = alt.layer(chart_reproduction_rate,
                                reproduction_selectors,
                                reproduction_points,
                                rule,
                                reproduction_text).properties(width=1050, height=400)
    return to_json(combinded_chart)


def to_json(chart):
    as_json = io.StringIO()
    chart.save(as_json, 'json')
    return as_json.getvalue()
