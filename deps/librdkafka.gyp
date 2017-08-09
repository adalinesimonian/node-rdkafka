{
  'variables': {
    'conditions': [
      [ 'OS=="win"', {
        "WITH_SASL%": "<!(IF DEFINED WITH_SASL (echo %WITH_SASL%) ELSE (echo 1))"
      }],
      [ 'OS!="win"', {
        "WITH_SASL%": "<!(echo ${WITH_SASL:-1})"
      }]
    ]
  },
  'targets': [
    {
      "target_name": "librdkafka_cpp",
      "type": "static_library",
      "include_dirs": [
        "librdkafka/src-cpp",
        "librdkafka/src"
      ],
      "dependencies": [
        "librdkafka"
      ],
      "conditions": [
        [ 'OS!="win"', {
          "sources": [ "<!@(find librdkafka/src-cpp -name *.cpp)", ],
        }],
        [ 'OS=="win"', {
          "sources": [ "<!@(..\\findwin librdkafka\\src-cpp *.cpp)", ],
          'configurations': {
            'Debug': {
              'msvs_settings': {
                'VCLinkerTool': {
                  'SetChecksum': 'true'
                },
                'VCCLCompilerTool': {
                  'RuntimeTypeInfo': 'true',
                  'RuntimeLibrary': '1', # /MTd
                  'InlineFunctionExpansion': 2 # /Ob2
                }
              },
            },
            'Release': {
              'msvs_settings': {
                'VCLinkerTool': {
                  'SetChecksum': 'true'
                },
                'VCCLCompilerTool': {
                  'RuntimeTypeInfo': 'true',
                  'RuntimeLibrary': '0', # /MT
                  'InlineFunctionExpansion': 2 # /Ob2
                }
              },
            }
          },
          'defines': [
            'LIBRDKAFKA_STATICLIB'
          ]
        }],
        [
          'OS=="linux"',
          {
            'cflags_cc!': [
              '-fno-rtti'
            ],
            'cflags_cc' : [
              '-Wno-sign-compare',
              '-Wno-missing-field-initializers',
              '-Wno-empty-body',
            ],
          }
        ],
        ['OS=="mac"', {
          'xcode_settings': {
            'OTHER_CFLAGS': [
              '-ObjC'
            ],
            'MACOSX_DEPLOYMENT_TARGET': '10.7',
            'GCC_ENABLE_CPP_RTTI': 'YES',
            'OTHER_CPLUSPLUSFLAGS': [
              '-std=c++11',
              '-stdlib=libc++'
            ],
            'OTHER_LDFLAGS': [],
          },
          'defines': [
            'FWD_LINKING_REQ'
          ]
        }]
      ]
    },
    {
      "target_name": "librdkafka",
      "type": "static_library",
      'defines': [
         'HAVE_CONFIG_H'
      ],
      "include_dirs": [
        "librdkafka/src"
      ],
      'cflags': [
        '-Wunused-function',
        '-Wformat',
        '-Wimplicit-function-declaration'
      ],
      "conditions": [
        [
          'OS=="linux"',
          {
            'cflags!': [
            ],
            'cflags' : [
              '-Wno-type-limits',
              '-Wno-unused-function',
              '-Wno-maybe-uninitialized',
              '-Wno-sign-compare',
              '-Wno-missing-field-initializers',
              '-Wno-empty-body',
              '-Wno-old-style-declaration',
            ],
            "dependencies": [
              "librdkafka_config"
            ]
          }
        ],
        [
          'OS=="mac"',
          {
            'xcode_settings': {
              'OTHER_CFLAGS' : [
                '-Wno-sign-compare',
                '-Wno-missing-field-initializers',
                '-ObjC',
                '-Wno-implicit-function-declaration',
                '-Wno-unused-function',
                '-Wno-format'
              ],
              'OTHER_LDFLAGS': [],
              'MACOSX_DEPLOYMENT_TARGET': '10.11',
              'libraries' : ['-lz']
            },
            "dependencies": [
                "librdkafka_config"
            ]
          }
        ],
        [
          'OS=="win"',
          {
            'configurations': {
              'Debug': {
                'msvs_settings': {
                  'VCLinkerTool': {
                    'SetChecksum': 'true'
                  },
                  'VCCLCompilerTool': {
                    'RuntimeTypeInfo': 'true',
                    'RuntimeLibrary': '1', # /MTd
                    'InlineFunctionExpansion': 2 # /Ob2
                  }
                },
              },
              'Release': {
                'msvs_settings': {
                  'VCLinkerTool': {
                    'SetChecksum': 'true'
                  },
                  'VCCLCompilerTool': {
                    'RuntimeTypeInfo': 'true',
                    'RuntimeLibrary': '0', # /MT
                    'InlineFunctionExpansion': 2 # /Ob2
                  }
                },
              }
            }
          }
        ],
        [ 'OS!="win" and <(WITH_SASL)==1',
          {
            'sources': [
              '<!@(find librdkafka/src -name rdkafka_sasl*.c ! -name rdkafka_sasl_win32*.c )'
            ]
          }
        ],
        [ 'OS=="win" and <(WITH_SASL)==1',
          {
            'sources': [
              "<!@(..\\findwin librdkafka\\src rdkafka_sasl*.c rdkafka_sasl_cyrus)"
            ]
          }
        ],
        [ 'OS!="win"', {
          "sources": [ '<!@(find librdkafka/src -name *.c ! -name rdkafka_sasl* )', ],
          'cflags!': [ '-fno-rtti' ]
        }],
        [ 'OS=="win"', {
          "sources": [ "<!@(..\\findwin librdkafka\\src *.c rdkafka_sasl)", ]
        }]
      ],
    },
    {
      "target_name": "librdkafka_config",
      "type": "none",
      "actions": [
        {
          'action_name': 'configure_librdkafka',
          'message': 'configuring librdkafka...',
          'inputs': [
            'librdkafka/configure',
          ],
          'outputs': [
            'librdkafka/config.h',
          ],
          "conditions": [
            [ 'OS!="win"',
              {
                "conditions": [
                  [ "<(WITH_SASL)==1",
                    {
                      'action': ['eval', 'cd librdkafka && chmod a+x ./configure && ./configure']
                    },
                    {
                      'action': ['eval', 'cd librdkafka && chmod a+x ./configure && ./configure --disable-sasl']
                    }
                  ]
                ]
              },
              {
                'action': ['echo']
              }
            ]
          ]
        }
      ]
    }
  ]
}
