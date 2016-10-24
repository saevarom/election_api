(function() {
  (function($) {
    return $.widget('IKS.subbutton', {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;

        widget = this;
        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Supscript',
          icon: 'icon icon-fa-subscript',
          command: null
        });
        toolbar.append(button);
        return button.on('click', function(event) {
          var insertionPoint, lastSelection;

          lastSelection = widget.options.editable.getSelection();
          insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
                    var elem;
                    elem = '<sub>' + lastSelection + '</sub>';

                    var node = lastSelection.createContextualFragment(elem);

                    lastSelection.deleteContents();
                    lastSelection.insertNode(node);

                    return widget.options.editable.element.trigger('change');
        });
      }
    });
  })(jQuery);

}).call(this);

(function() {
  (function($) {
    return $.widget('IKS.supbutton', {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;

        widget = this;
        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Superscript',
          icon: 'icon icon-fa-superscript',
          command: null
        });
        toolbar.append(button);
        return button.on('click', function(event) {
          var insertionPoint, lastSelection;

          lastSelection = widget.options.editable.getSelection();
          insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
                    var elem;
                    elem = '<sup>' + lastSelection + '</sup>';

                    var node = lastSelection.createContextualFragment(elem);

                    lastSelection.deleteContents();
                    lastSelection.insertNode(node);

                    return widget.options.editable.element.trigger('change');
        });
      }
    });
  })(jQuery);
  
}).call(this);


(function() {
  (function(jQuery) {
    return jQuery.widget("IKS.hallojustifyovercast", {
      options: {
        editable: null,
        toolbar: null,
        uuid: '',
        buttonCssClass: null
      },
      populateToolbar: function(toolbar) {
        var buttonize, buttonset,
          _this = this;
        buttonset = jQuery("<span class=\"" + this.widgetName + "\"></span>");
        buttonize = function(alignment) {
          var buttonElement;
          buttonElement = jQuery('<span></span>');
          buttonElement.hallobutton({
            uuid: _this.options.uuid,
            editable: _this.options.editable,
            label: alignment,
            command: "justify" + alignment,
            icon: "icon icon-fa-align-" + (alignment.toLowerCase()),
            cssClass: _this.options.buttonCssClass
          });
          return buttonset.append(buttonElement);
        };
        buttonize("Left");
        buttonize("Center");
        buttonize("Right");
        buttonset.hallobuttonset();
        return toolbar.append(buttonset);
      }
    });
  })(jQuery);

}).call(this);

(function() {
  (function(jQuery) {
    return jQuery.widget("IKS.hallohtmlovercast", {
      options: {
        editable: null,
        toolbar: null,
        uuid: "",
        lang: 'en',
        dialogOpts: {
          autoOpen: false,
          width: 600,
          height: 'auto',
          modal: false,
          resizable: true,
          draggable: true,
          dialogClass: 'htmledit-dialog'
        },
        dialog: null,
        buttonCssClass: null
      },
      translations: {
        en: {
          title: 'Edit HTML',
          update: 'Update'
        },
        de: {
          title: 'HTML bearbeiten',
          update: 'Aktualisieren'
        }
      },
      texts: null,
      populateToolbar: function($toolbar) {
        var $buttonHolder, $buttonset, id, selector, widget;
        widget = this;
        this.texts = this.translations[this.options.lang];
        this.options.toolbar = $toolbar;
        selector = "" + this.options.uuid + "-htmledit-dialog";
        this.options.dialog = jQuery("<div>").attr('id', selector);
        $buttonset = jQuery("<span>").addClass(widget.widgetName);
        id = "" + this.options.uuid + "-htmledit";
        $buttonHolder = jQuery('<span>');
        $buttonHolder.hallobutton({
          label: this.texts.title,
          icon: 'icon icon-fa-code',
          editable: this.options.editable,
          command: null,
          queryState: false,
          uuid: this.options.uuid,
          cssClass: this.options.buttonCssClass
        });
        $buttonset.append($buttonHolder);
        this.button = $buttonHolder;
        this.button.click(function() {
          if (widget.options.dialog.dialog("isOpen")) {
            widget._closeDialog();
          } else {
            widget._openDialog();
          }
          return false;
        });
        this.options.editable.element.on("hallodeactivated", function() {
          return widget._closeDialog();
        });
        $toolbar.append($buttonset);
        this.options.dialog.dialog(this.options.dialogOpts);
        return this.options.dialog.dialog("option", "title", this.texts.title);
      },
      _openDialog: function() {
        var $editableEl, html, widget, xposition, yposition,
          _this = this;
        widget = this;
        $editableEl = jQuery(this.options.editable.element);
        xposition = $editableEl.offset().left + $editableEl.outerWidth() + 10;
        yposition = this.options.toolbar.offset().top - jQuery(document).scrollTop();
        this.options.dialog.dialog("option", "position", [xposition, yposition]);
        this.options.editable.keepActivated(true);
        this.options.dialog.dialog("open");
        this.options.dialog.on('dialogclose', function() {
          jQuery('label', _this.button).removeClass('ui-state-active');
          _this.options.editable.element.focus();
          return _this.options.editable.keepActivated(false);
        });
        this.options.dialog.html(jQuery("<textarea>").addClass('html_source'));
        html = this.options.editable.element.html();
        this.options.dialog.children('.html_source').val(html);
        this.options.dialog.prepend(jQuery("<button>" + this.texts.update + "</button>"));
        return this.options.dialog.on('click', 'button', function() {
          html = widget.options.dialog.children('.html_source').val();
          widget.options.editable.element.html(html);
          widget.options.editable.element.trigger('change');
          return false;
        });
      },
      _closeDialog: function() {
        return this.options.dialog.dialog("close");
      }
    });
  })(jQuery);

}).call(this);