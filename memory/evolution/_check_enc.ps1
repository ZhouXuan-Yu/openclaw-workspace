$p = 'C:\Users\ZhouXuan\.openclaw\workspace\memory\evolution\evolution-log.md'
$bytes = [System.IO.File]::ReadAllBytes($p)
# find byte offset of "2026-07-28" then show next 60 bytes as hex
$needle = [System.Text.Encoding]::ASCII.GetBytes('2026-07-28')
$idx = -1
for ($i = 0; $i -le $bytes.Length - $needle.Length; $i++) {
  $match = $true
  for ($j = 0; $j -lt $needle.Length; $j++) {
    if ($bytes[$i+$j] -ne $needle[$j]) { $match = $false; break }
  }
  if ($match) { $idx = $i; break }
}
Write-Output ("Found at: " + $idx)
$hex = ($bytes[($idx+12)..($idx+80)] | ForEach-Object { $_.ToString('X2') }) -join ' '
Write-Output ("Hex: " + $hex)
