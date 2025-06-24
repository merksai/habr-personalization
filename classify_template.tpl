<!-- classify_template.tpl -->
<!DOCTYPE html>
<html>
  <head>
    <link
      rel="stylesheet"
      href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"
    />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
  </head>
  <body>
    <div class="ui container" style="padding-top: 10px;">
      <h2 class="ui header">Рекомендации по новостям</h2>
      <table class="ui celled table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Complexity</th>
            <th>Recommendation</th>
          </tr>
        </thead>
        <tbody>
          % for item, lbl in rows:
            % if lbl == 'good':
              <tr class="positive">
            % elif lbl == 'maybe':
              <tr class="active">
            % else:
              <tr class="negative">
            % end
                <td>
                  <a href="{{item.url}}" target="_blank">{{item.title}}</a>
                </td>
                <td>{{item.author}}</td>
                <td>{{item.complexity}}</td>
                <td>
                  % if lbl == 'good':
                    <i class="thumbs up icon"></i> Интересно
                  % elif lbl == 'maybe':
                    <i class="help circle icon"></i> Возможно
                  % else:
                    <i class="thumbs down icon"></i> Не интересно
                  % end
                </td>
              </tr>
          % end
        </tbody>
        <tfoot class="full-width">
          <tr>
            <th colspan="4">
              <a href="/news" class="ui small button">
                ← Вернуться к разметке
              </a>
              <a href="/update_news" class="ui right floated small primary button">
                Больше новостей!
              </a>
            </th>
          </tr>
        </tfoot>
      </table>
    </div>
  </body>
</html>