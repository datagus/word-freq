# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "altair==6.0.0",
#     "marimo",
#     "pandas==2.3.3",
# ]
# ///
import marimo

__generated_with = "0.19.6"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import marimo as mo
    import altair as alt
    return alt, mo, pd


@app.cell
def _():
    #mo.md("""## Loading again dataframe and clus_df""")
    return


@app.cell
def _(mo):
    mo.md("""
    # Generative Artificiall Intelligence and Behavior change, Sustainability and Policy
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ------
    """)
    return


@app.cell
def _(mo):

    info_box = mo.Html("""
    <div style="
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 20px;
        border-radius: 4px;
        font-family: system-ui, -apple-system, sans-serif;
    ">
        <h3 style="margin-top: 0; color: #1565c0;">Data Processing Summary</h3>
        <ul style="line-height: 1.8; color: #333;">
            <li><strong>Raw abstract sample:</strong> 3,380 words from 711 abstracts</li>
            <li><strong>Removed words:</strong> "review", "article", "finding", "conclusion", "study", "research", "question", "paper", "result", "method"</li>
            <li><strong>Filtering criterion:</strong> Incidence > 1</li>
            <li><strong>Final word count:</strong> 1,935 words</li>
        </ul>
    </div>
    """)

    info_box
    return


@app.cell
def _(mo):
    # Display an image from a file path
    dendogram = mo.image("images/dendogram.jpg")
    indicators = mo.image("images/indicators.jpg")
    wordcloud = mo.image("images/wordcloud.jpg")
    return dendogram, indicators, wordcloud


@app.cell
def _(dendogram, indicators, mo, wordcloud):
    mo.vstack([
        mo.md("**Expand and collapse to see the different outputs from the wordination package**"),
        mo.accordion({
            "📈 Indicators": indicators,
            "📊 Dendogram": dendogram,
            "☁️ Word Cloud": wordcloud
        })
    ])
    return


@app.cell
def _(pd):
    all_df = pd.read_csv("eurofound.csv")
    all_df["short_id"] = all_df.index + 1
    all_df = all_df.iloc[:,1:]
    #all_df
    return (all_df,)


@app.cell
def _(pd):
    clus_df = pd.read_csv("eurofound_clust.csv")
    clus_df["article"] = clus_df["article"].str[:-4].astype(int)
    clus_df = clus_df.rename(columns={"article": "short_id"})
    #clus_df
    return (clus_df,)


@app.cell
def _(all_df, clus_df, pd):
    final = pd.merge(all_df,clus_df, on="short_id", how="inner")
    final["cluster_number"] = final["cluster_number"].astype('str')
    #final.loc[final["cluster_number"].isna(),"cluster_number"] = "no group"
    #final.loc[final["words"].isna(),"words"] = "removed from R analysis"
    #final
    return (final,)


@app.cell
def _(pd):
    moritz = pd.read_csv("moritz_good.csv")
    #moritz
    return (moritz,)


@app.cell
def _(pd):
    abundance = pd.read_csv("abundance.csv")
    abundance.columns.values[0] = "words"
    #abundance
    return (abundance,)


@app.cell(hide_code=True)
def _(mo):
    usage_info_box = mo.Html("""
    <div style="
        background-color: #fff9c4;
        border-left: 4px solid #fbc02d;
        padding: 20px;
        border-radius: 4px;
        font-family: system-ui, -apple-system, sans-serif;
    ">
        <h3 style="margin-top: 0; color: #f57f17;">📝 How to Explore Word Frequencies</h3>
        <p style="line-height: 1.8; color: #333; margin: 10px 0;">
            Type words to explore their frequency across different articles. You can add more than one word by separating them with commas.
        </p>
        <p style="line-height: 1.8; color: #333; margin: 10px 0;">
            Use these to choose words:
        </p>
        <ul style="line-height: 1.8; color: #333;">
            <li><strong>Incidence and Total Abundance Table</strong> - see word frequencies and total abundances</li>
            <li><strong>Word Cloud</strong> - locate in the dca the words</li>
        </ul>
    </div>
    """)

    usage_info_box
    return


@app.cell
def _(abundance, final, mo, moritz):
    # Create an accordion with multiple dataframes
    accordion = mo.accordion({
        "Final merged data": final,
        "Abundance table": abundance,
        "Incidence and total abundance table": moritz
    })

    mo.vstack([
        mo.md("**Expand and collapse to see the tables below**"), accordion
    ])
    return


@app.cell
def _(mo):
    # Create a text input for word search
    word_search = mo.ui.text(
        value="",
        label="Enter words (comma-separated)",
        placeholder="e.g., application, care, data",
        full_width=True
    )

    # Wrap in a styled container
    styled_search = mo.Html(f"""
    <div style="
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h3 style="
            margin-top: 0;
            margin-bottom: 15px;
            color: #7b1fa2;
            font-family: system-ui, -apple-system, sans-serif;
            font-size: 1.1em;
        ">🔍 Search Words</h3>
        {word_search}
    </div>
    """)

    styled_search
    return (word_search,)


@app.cell
def _(abundance, final, mo, pd, word_search):
    # Process the search and create subselected dataframe
    if word_search.value.strip():
        # Split words by comma and strip whitespace
        search_words = [word.strip().lower() for word in word_search.value.split(",") if word.strip()]
    
        # Filter rows where 'words' column matches any of the search words
        filtered_df = abundance[abundance["words"].str.lower().isin(search_words)]
    
        if not filtered_df.empty:
            # Get columns where at least one value is > 0
            cols_to_keep = ["words"]  # Always keep the words column
        
            for col in abundance.columns[1:]:  # Skip the first column (words)
                # If multiple words searched, check if ALL words have count > 1
                if len(search_words) > 1:
                    if (filtered_df[col] > 1).all():  # ALL words must have count > 1
                        cols_to_keep.append(col)
                else:
                    # For single word, keep if count > 0
                    if (filtered_df[col] > 0).any():
                        cols_to_keep.append(col)
        
            # Subset and transpose
            if len(cols_to_keep) > 1:
                # Subset and transpose
                xdf = filtered_df[cols_to_keep].set_index("words").T
                xdf = xdf.reset_index(drop=False, names="words")
                xdf["words"] = xdf["words"].str[:-4].astype(int)
                xdf = xdf.rename(columns={"words": "short_id"})
                subselected_df = pd.merge(final,xdf, on="short_id", how="inner")

                #mo.md(f"**Found {len(filtered_df)} word(s) with {len(cols_to_keep)-1} documents containing them**")
        
            else:
                subselected_df = pd.DataFrame()
                mo.md("**No documents found where all words appear more than once**")
        else:
            subselected_df = pd.DataFrame()
            mo.md("**No matching words found**")
    else:
        subselected_df = pd.DataFrame()
        mo.md("**Enter words to search**")

    subselected_df
    return search_words, subselected_df


@app.cell
def _(alt, search_words, subselected_df, word_search):
    _search_words = [word.strip().lower() for word in word_search.value.split(",") if word.strip()]
    
    # Prepare data for plotting by melting the dataframe
    plot_data = subselected_df[['short_id'] + search_words].melt(
        id_vars=['short_id'],
        var_name='word',
        value_name='count'
    )

    plot_data = plot_data[plot_data['count'] > 0]

    # Create the count plot
    _chart = alt.Chart(plot_data).mark_bar().encode(
        x=alt.X('short_id:O', title='Document ID (short_id)', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('count:Q', title='Word Count'),
        color=alt.Color('word:N', title='Word', legend=alt.Legend(orient='right')),
        tooltip=['short_id:O', 'word:N', 'count:Q']
    ).properties(
        title=f'Word Frequency by Document: {", ".join(search_words)}',
        width=600,
        height=400
    )

    _chart
    return


if __name__ == "__main__":
    app.run()
