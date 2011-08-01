<script ns1:version="11.01" id="custom-script">
    var refresh_period = 60;
    var iters_until_reload = 10;

    function refresh_images()
    {
        var rand = Math.floor(Math.random()*1000000);
        var images = document.getElementsByTagName('image');

        for (var i = 0, len = images.length; i &lt; len; i++) {
            var img = images.item(i);
            var src = img.getAttribute('xlink:href');

            if (/rnd=/.test(src)) {
                src = src.replace(/rnd=[0-9]+/,  'rnd=' + rand);
            } else {
                if (/\?/.test(src)) {
                    src = src + '&amp;rnd=' + rand;
                } else {
                    src = src + '?rnd=' + rand;
                }
            }
            img.setAttribute('xlink:href', src)
        }

        iters_until_reload--;
        if (iters_until_reload == 0) {
            window.location.href = window.location.href.replace(/#.*/, '');
        } else {
            window.setTimeout(refresh_images, refresh_period * 1000);
        }
    }
    window.setTimeout(refresh_images, refresh_period * 1000);
</script>

