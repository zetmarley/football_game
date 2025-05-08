<script>
  document.getElementById('player').addEventListener('input', function() {
    fetch('/player-autocomplete/?q=' + this.value)
      .then(response => response.json())
      .then(data => {
        const datalist = document.getElementById('players');
        datalist.innerHTML = '';
        data.forEach(name => {
          const option = document.createElement('option');
          option.value = name;
          datalist.appendChild(option);
        });
      });
  });
</script>