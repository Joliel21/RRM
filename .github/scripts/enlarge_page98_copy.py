from pathlib import Path

path = Path('src/app/components/ReadingView.tsx')
text = path.read_text(encoding='utf-8')

marker = '''      ) : null}\n\n{seriesTheme ? (\n'''

insert = '''      ) : null}\n\n      {page.id === "a-day-in-life-intro-page" ? (\n        <div\n          className="pointer-events-none absolute z-[140] overflow-hidden"\n          style={{\n            left: "9.5%",\n            right: "7.5%",\n            top: "55.7%",\n            bottom: "6.8%",\n            background: "#f9f8f5",\n            color: "#222222",\n            fontFamily: "Arial, Helvetica, sans-serif",\n          }}\n        >\n          <div\n            className="grid h-full"\n            style={{\n              gridTemplateColumns: "52% 48%",\n              fontSize: "19px",\n              lineHeight: 1.43,\n            }}\n          >\n            <div className="flex h-full flex-col" style={{ paddingRight: "30px" }}>\n              <p style={{ margin: 0, marginBottom: "22px" }}>\n                First-person accounts from people living with rare conditions, family members, caregivers, advocates and professionals.\n              </p>\n              <p style={{ margin: 0 }}>\n                These personal accounts bring the realities of rare disease into sharper focus, exploring how diagnosis, treatment and uncertainty can shape everyday routines, relationships, careers, education, independence and identity. They reveal the practical challenges, difficult decisions, unexpected adaptations and meaningful moments that clinical descriptions often leave out.\n              </p>\n              <div\n                style={{\n                  marginTop: "22px",\n                  borderTop: "2px solid #C99B38",\n                  paddingTop: "16px",\n                  color: "#C99B38",\n                  fontFamily: "Georgia, 'Times New Roman', serif",\n                  fontSize: "27px",\n                  fontWeight: 700,\n                  lineHeight: 1.08,\n                }}\n              >\n                Real stories. Real perspectives.<br />\n                Real impact.\n              </div>\n            </div>\n            <div\n              style={{\n                borderLeft: "2px solid #C99B38",\n                paddingLeft: "38px",\n              }}\n            >\n              <p style={{ margin: 0, marginBottom: "22px" }}>\n                They reveal the practical challenges, difficult decisions, unexpected adaptations and meaningful moments that clinical descriptions often leave out.\n              </p>\n              <p style={{ margin: 0, marginBottom: "22px" }}>\n                By centering the voices of those directly affected, A Day in the Life shows the person beyond the condition and the full life surrounding it.\n              </p>\n              <p style={{ margin: 0 }}>\n                Together, these stories move beyond awareness to build understanding, challenge assumptions and place the human experience at the forefront.\n              </p>\n            </div>\n          </div>\n        </div>\n      ) : null}\n\n{seriesTheme ? (\n'''

if 'page.id === "a-day-in-life-intro-page"' in text:
    raise SystemExit('Page 98 overlay already exists')

if marker not in text:
    raise SystemExit('Static image insertion marker not found')

text = text.replace(marker, insert, 1)
path.write_text(text, encoding='utf-8')
