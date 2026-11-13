# Video types

Every Short has exactly one type. The scriptwriter puts it at the top of scripts/<slug>.md as `type: <name>`,
and every agent reads the matching style file before working.

| Type | File | Visuals come from | Chris's part | Max length |
|---|---|---|---|---|
| fragrance | fragrance.md | Chris films | face/hands + voice | 60s |
| gaming | gaming.md | Chris's gameplay capture | voiceover/commentary | 60s |
| faceless | faceless.md | code-built 3D simulation (animator) | script choices + voiceover | 60s |
| brainrot | brainrot.md | AI image → video clips (animator prompt pack) | jokes/story picks + at least one voice | 90s |

The max length is enforced by tools/check-renders.sh.
